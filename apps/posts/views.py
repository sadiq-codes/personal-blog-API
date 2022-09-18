from routes import api
from flask import request, jsonify, abort, make_response
from flask_jwt_extended import current_user, jwt_required
from .. import db
from .forms import PostForm, TagForm
from .models import Post, Tag


@api.route('/create/post', methods=['POST'])
@jwt_required()
def create_post():
    form = PostForm(request.form)
    if form.is_submitted():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        tags_data = form.tags.data
        tags = []
        # if tags_data:
        #     for tag in tags:
        #         if Tag.query.filter_by(slug=tag.slug).first():
        #             return make_response("tag already exist")
        #         else:
        #             tags.append(db.session.add(Tag(name=))
        #
        db.session.add(post)
        db.session.commit()
        return jsonify(post.format_to_json()), 200


@api.route('/post/update/<post_slug>', methods=['PUT'])
@jwt_required()
def update_post(post_slug):
    title = request.json.get("title", None)
    body = request.json.get("body", None)
    tags = request.json.get("tags", None)

    post = Post.query.get_or_404(slug=post_slug).first()

    if current_user != post.author:
        abort(404)
    else:
        post.title = title
        post.body = body
        if tags:
            post.tags = tags
        db.session.add(post)
        db.session.commit()
    return jsonify(post.format_to_json())


@api.route('/delete/<post_slug>', methods=['DELETE'])
@jwt_required()
def delete_post(post_slug):
    post = Post.query.get_or_404(slug=post_slug)
    if current_user != post.author:
        return False
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "post deleted successfully"}), 200


@api.route('/blogs/list', methods=['GET'])
def post_list():
    posts = Post.query.all()
    return jsonify({'posts': [post.format_to_json() for post in posts]})


@api.route('/blog/detail/<post_slug>', methods=['GET'])
def post_detail(post_slug):
    post = Post.query.first_or_404(slug=post_slug)
    return jsonify(post.format_to_json())


@api.route('/create/tag', methods=['POST'])
@jwt_required()
def create_tag():
    form = TagForm(request.form)
    if form.is_submitted():
        tag = Tag(name=form.name.data, description=form.description.name)
        db.session.add(tag)
        db.session.commit()
        return make_response(f"tag {tag.name} successfully added"), 200
    else:
        return make_response("form is invalid")
    return jsonify({"message": "add tag"})


@api.route('update/tag/<tag_slug>', methods=['PUT'])
@jwt_required()
def update_tag(tag_slug):
    name = request.json.get('name', None)
    description = request.json.get('description', None)

    tag = Tag.query.get_or_404(slug=tag_slug)
    tag.name = name
    tag.description = description
    return jsonify(tag.format_to_json())


@api.route('/delete/tag/<tag_slug>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_slug):
    tag = Tag.query.get_or_404(slug=tag_slug)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "tag deleted successfully"}), 200


@api.route('/post/<tag_slug>', methods=['GET'])
def get_post_by_tag(tag_slug):
    tag = Tag.query.first_or_404(slug=tag_slug)
    posts = tag.posts.order_by(Tag.id)
    return jsonify({'posts': [post.format_to_json() for post in posts]})

# def get_or_create(db, model, **kwargs):
#     instance = model.query.filter_by(**kwargs).first()
#     if instance:
#         return instance, False
#     else:
#         create_instance = model(dict(k, v) for k,v in **kwargs)
#
