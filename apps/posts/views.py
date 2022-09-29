from routes import api
import random
from flask import request, jsonify, abort, make_response, current_app, url_for
from flask_jwt_extended import current_user, jwt_required, get_csrf_token
from .. import db
from sqlalchemy import update, func
from .forms import PostForm, TagForm
from .models import Post, Tag
from ..errors import bad_request, forbidden, method_not_allowed, not_found
from ..helpers import get_or_create


@api.route('/post/create', methods=['POST'])
@jwt_required()
def create_post():
    form = PostForm(request.form)
    if form.is_submitted():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        tags_data = form.tags.data
        tags_data = tags_data.split(',')
        print(tags_data)
        if tags_data:
            for tag in tags_data:
                new_tag = get_or_create(db, Tag, name=tag)
                new_tag.posts.append(post)
        db.session.add(post)
        db.session.commit()
        return jsonify(post.format_to_json()), 200


@api.route('/post/update/<post_slug>', methods=['PUT'])
@jwt_required()
def update_post(post_slug):
    title = request.json.get("title", None)
    body = request.json.get("body", None)
    tags = request.json.get("tags", None)

    post = Post.query.get_or_404(post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")

    if current_user != post.author:
        forbidden(message="Permission denied")
    else:
        post.title = title
        post.body = body
        tags_data = tags.split(',')
        if tags_data:
            for tag in tags_data:
                new_tag = get_or_create(db, Tag, name=tag)
                new_tag.posts.append(post)
        db.session.add(post)
        db.session.commit()
    return jsonify(post.format_to_json())


@api.route('/post/delete/<post_slug>', methods=['DELETE'])
@jwt_required()
def delete_post(post_slug):
    post = Post.query.get_or_404(slug=post_slug)
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
        .paginate(page, per_page=8,
                  error_out=False)
    posts_item = posts.items

    prev_post = None
    if posts.has_prev:
        prev_post = url_for('api.post_list', page=page - 1)

    next_post = None
    if posts.has_next:
        next_post = url_for('api.post_list', page=page + 1)

    return jsonify({
        'posts': [post.format_to_json() for post in posts_item],
        'prev_url': prev_post,
        'next_url': next_post,
        'count': posts.total
    })


@api.route('/post/detail/<post_slug>', methods=['GET'])
@jwt_required(optional=True)
def post_detail(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return not_found(message=f"post with slug {post_slug} does not exist")
    return jsonify({"post": post.format_to_json()})


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
    tag = Tag.query.get_or_404(tag_slug)
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
    # db.session.delete(tag)
    # db.session.commit()
    return jsonify({"tags": tag_list}), 200


@api.route('/tags/<tag_slug>', methods=['GET'])
def get_post_by_tags(tag_slug):
    tag1 = Tag.query.filter_by(slug=tag_slug).first()
    posts = tag1.posts
    return jsonify({'posts': [post.format_to_json() for post in posts]})


@api.route('/posts/featured', methods=['GET'])
def featured():
    posts = Post.query.order_by(Post.updated_on.desc()).all()
    posts = posts[7:8]
    post = random.choice(posts)
    return jsonify(post.format_to_json())


@api.route('posts/updated', methods=['GET'])
def updated_posts():
    posts = Post.query.order_by(Post.updated_on.desc()).all()
    posts = posts[:5]
    return jsonify({'posts': [post.format_to_json() for post in posts]})
