from routes import api
import random
from flask import request, jsonify, make_response, url_for, current_app, \
    send_from_directory
from flask_jwt_extended import current_user, jwt_required, get_csrf_token
from apps import db, photos
from PIL import Image
from .forms import PostForm, TagForm, CategoryForm
from .models import Post, Tag, Category, tag
from ..errors import bad_request, forbidden, method_not_allowed, not_found
from ..helpers import get_or_create, destination_save, destination_open, add_to_digitalocean
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func


@api.route('/create/category', methods=['POST'])
@jwt_required()
def create_category():
    form = CategoryForm(request.form)
    if form.is_submitted():
        category = Category(name=form.name.data.lower(),
                            description=form.description.name)
        db.session.add(category)
        db.session.commit()
        return make_response(f"category {category.name} successfully added"), 200
    else:
        return make_response("form is invalid")


@api.route('/category/update/<category_slug>', methods=['PUT'])
@jwt_required()
def update_category(category_slug):
    category_name = request.json.get('category_name', None)
    category_description = request.json.get('category_description', None)

    category = Category.query.get_or_404(category_slug)
    if not category:
        return not_found(message=f"category with slug {category_slug} does not exist")
    category.name = category_name
    category.description = category_description
    db.session.add(category)
    db.session.commit()
    return jsonify(category.format_to_json()), 200


@api.route('/category/delete/<category_slug>', methods=['DELETE'])
@jwt_required()
def delete_category(category_slug):
    category = Tag.query.filter_by(slug=category_slug).first()
    if not category:
        return not_found(message=f"post with slug {category_slug} does not exist")
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "tag deleted successfully"}),


@api.route('/category/list', methods=['GET'])
def get_category():
    categories = Category.query.order_by(Category.name)
    return jsonify({"categories": [category.format_to_json(add_post=False) for category in categories]})


@api.route('/category/<category_slug>', methods=['GET'])
def get_post_by_category(category_slug):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(slug=category_slug).first()
    posts = category.post.order_by(Post.publish_on.desc()) \
        .paginate(page, per_page=16,
                  error_out=False)

    prev_post = url_for('api.post_list', page=posts.prev_num) \
        if posts.has_prev else None

    next_post = url_for('api.post_list', page=posts.next_num) \
        if posts.has_next else None

    return jsonify({
        'posts': [post.format_to_json() for post in posts.items],
        'prev_url': prev_post,
        'next_url': next_post,
        'count': posts.total
    })


@api.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PHOTOS_DEST"], secure_filename(filename))


@api.route('/post/create', methods=['POST'])
@jwt_required(optional=True)
def create_post():
    form = PostForm(request.form)
    if form.is_submitted() and 'photo' in request.files:
        category = get_or_create(db, Category, name=request.form["category"].lower())
        post = Post(title=form.title.data, body=form.body.data, author=current_user, category=category)

        file = request.files['photo']
        if request.files and file.filename != "":
            # for local host
            # photo = photos.save(request.files['photo'])
            # image = Image.open(destination_open(photo))
            # image.thumbnail((2400, 1600))
            # image.save(destination_save(photo))
            # post.image = photo

            # for digital ocean spaces
            add_to_digitalocean(file)

        tags_data = form.tags.data.split(',')
        if tags_data:
            for tag in tags_data:
                new_tag = get_or_create(db, Tag, name=tag)
                new_tag.posts.append(post)
        db.session.add(post)
        db.session.commit()
        return jsonify(post.format_to_json()), 200
    return jsonify({"msg": "add post data to create"})


@api.route('/post/update/<post_slug>', methods=['PUT'])
@jwt_required(optional=True)
def update_post(post_slug):
    form = PostForm(request.form)
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")

    if current_user != post.author:
        forbidden(message="Permission denied")
    else:
        category = get_or_create(db, Category, name=request.form["category"].lower())
        file = request.files['photo']
        if request.files and file.filename != "":
            # for local host
            # photo = photos.save(request.files['photo'])
            # image = Image.open(destination_open(photo))
            # image.thumbnail((2400, 1600))
            # image.save(destination_open(photo))
            # post.image = photo

            # for digital ocean spaces
            add_to_digitalocean(file)
            post.image = file.filename
        post.category = category
        post.title = form.title.data
        post.body = form.body.data
        tags_data = form.tags.data.split(',')
        tags_array = []
        if tags_data:
            for tag in tags_data:
                new_tag = get_or_create(db, Tag, name=tag.lower())
                # if new_tag not in post.tags:
                #     new_tag.posts.append(post)
                tags_array.append(new_tag)
                post.tags = tags_array
        db.session.add(post)
        db.session.commit()
    return jsonify(post.format_to_json())


@api.route('/post/delete/<post_slug>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")
    if current_user != post.author:
        forbidden(message="Permission denied")
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "post deleted successfully"}), 200


@api.route('/posts/list', methods=['GET'])
def post_list():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.publish_on.desc()) \
        .paginate(page, per_page=16,
                  error_out=False)

    prev_post = url_for('api.post_list', page=posts.prev_num) \
        if posts.has_prev else None

    next_post = url_for('api.post_list', page=posts.next_num) \
        if posts.has_next else None

    return jsonify({
        'posts': [post.format_to_json() for post in posts.items],
        'prev_url': prev_post,
        'next_url': next_post,
        'count': posts.total
    })


@api.route('/post/detail/<post_slug>', methods=['GET'])
@jwt_required(optional=True)
def post_detail(post_slug):
    print(post_slug)
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")

    tags_ids = db.session.query(tag.c.tags_id).filter(tag.c.posts_id == post.id)
    posts = db.session.query(Post) \
                .filter(Post.id != post.id) \
                .filter(tag.c.tags_id.in_(tags_ids)) \
                .filter(tag.c.posts_id == Post.id) \
                .group_by(Post) \
                .order_by(func.count(tag.c.tags_id).desc()).all()[:3]

    return jsonify({"post": post.format_to_json(),
                    "related": [p.format_to_json() for p in posts]})


@api.route('/create/tag', methods=['POST'])
@jwt_required()
def create_tag():
    form = TagForm(request.form)
    if form.is_submitted():
        tag = Tag(name=form.name.data,
                  description=form.description.name)
        db.session.add(tag)
        db.session.commit()
        return make_response(f"tag {tag.name} successfully added"), 200
    else:
        return make_response("form is invalid")


@api.route('/tag/update/<tag_slug>', methods=['PUT'])
@jwt_required()
def update_tag(tag_slug):
    name = request.json.get('name', None)
    description = request.json.get('description', None)

    tag = Tag.query.get_or_404(tag_slug)
    if not tag:
        return not_found(message=f"post with slug {tag_slug} does not exist")
    tag.name = name
    tag.description = description
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.format_to_json()), 200


@api.route('/tag/delete/<tag_slug>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_slug):
    tag = Tag.query.filter_by(slug=tag_slug).first()
    if not tag:
        return not_found(message=f"post with slug {tag_slug} does not exist")
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "tag deleted successfully"}),


@api.route('/tag/remove/<post_slug>/<tag_slug>', methods=['DELETE'])
@jwt_required()
def delete_post_tag(post_slug, tag_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")
    for tag in post.tags:
        if tag.slug == tag_slug:
            post.tags.remove(tag)
            db.session.commit()
    tag_list = [tag.slug for tag in post.tags]
    return jsonify({"tags": tag_list}), 200


@api.route('/tags/<tag_slug>', methods=['GET'])
def get_post_by_tags(tag_slug):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(slug=tag_slug).first()
    posts = tag.posts.order_by(Post.publish_on.desc()) \
        .paginate(page, per_page=16,
                  error_out=False)

    prev_post = url_for('api.post_list', page=posts.prev_num) \
        if posts.has_prev else None

    next_post = url_for('api.post_list', page=posts.next_num) \
        if posts.has_next else None

    return jsonify({
        'posts': [post.format_to_json() for post in posts.items],
        'prev_url': prev_post,
        'next_url': next_post,
        'count': posts.total
    })


@api.route('/posts/featured', methods=['GET'])
def featured():
    posts = Post.query.order_by(Post.updated_on.desc()).all()
    post = random.choice(posts)
    return jsonify(post.format_to_json())


@api.route('posts/updated', methods=['GET'])
def updated_posts():
    posts = Post.query.order_by(Post.updated_on.desc()).all()
    posts = posts[:5]
    return jsonify({'posts': [post.format_to_json() for post in posts]})
