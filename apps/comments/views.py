from routes import api
from flask import make_response, abort, request, jsonify, url_for
from .. import db
from flask_jwt_extended import jwt_required, current_user
from ..errors import not_found, bad_request
from sqlalchemy import desc

from .models import Comment, Like
from ..posts.models import Post


@api.route('/comment/create/<post_slug>', methods=['POST'])
def create_comment(post_slug):
    comment = request.json.get("comment", None)
    parent_id = request.json.get("comment_id", None)
    post = Post.query.filter_by(slug=post_slug).first()
    if post is None:
        return not_found(message=f"post with slug {post_slug} is not fund")
    if comment and parent_id:
        parent_comment = Comment.query.get(parent_id)
        if parent_comment is None:
            return not_found(message=f"comment with id {parent_id} not found")
        comment_reply = Comment(
            body=comment,
            post=post,
            author_id=1,
        )
        parent_comment.replies.append(comment_reply)
        db.session.add(comment_reply)
        db.session.commit()
        return jsonify({"message": "comment has been added successfully",
                        "comment": comment_reply.format_to_json()})

    elif comment and not parent_id:
        comment = Comment(
            body=comment,
            post=post,
            author_id=1,
        )
        db.session.add(comment)
        db.session.commit()

        return jsonify({"message": "comment has been added successfully",
                        "comment": comment.format_to_json()})
    return bad_request(message="comment field is empty")


@api.route('/comment/update/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment:
        return not_found(message="Comment to update not found")

    body = request.json.get('comment', None)
    if body:
        comment.body = body
        db.session.commit()
    return jsonify({"message": "comment updated successfully",
                    "comment": comment.format_to_json()})


@api.route('/comments/get/<post_slug>', methods=['GET'])
def get_comments(post_slug):
    page = request.args.get('page', 1, type=int)
    post_id = Post.query.filter_by(slug=post_slug).with_entities(Post.id).first()[0]
    if not post_id:
        return not_found(message=f"post with slug {post_slug} not found")

    comments = Comment.query.filter_by(post_id=post_id) \
        .order_by(desc(Comment.created_on)) \
        .paginate(page, per_page=35)
    comments_items = comments.items

    prev_comments = None
    if comments.has_prev:
        prev_comments = url_for('api.get_comments', post_slug=post_slug, page=page - 1)

    next_comments = None
    if comments.has_next:
        next_comments = url_for('api.get_comments', post_slug=post_slug, page=page + 1)

    return jsonify({
        'comments': [comment.format_to_json() for comment in comments_items],
        'prev_url': prev_comments,
        'next_url': next_comments,
        'comments_count': comments.total,
    })


@api.route('/comment/delete/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        return not_found(message="comment not found")
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment deleted successfully"})


@api.route('get/comments/likes/<post_slug>', methods=['GET'])
def get_comments_likes(post_slug):
    author_id = 1
    post = Post.query.filter_by(slug=post_slug).first()
    if post is None:
        return not_found(message=f"post with slug {post_slug} is not fund")

    has_like = False

    if Like.query.filter_by(author_id=author_id, post_id=post.id).count() > 0:
        has_like = True

    return jsonify({"post": {"likes": post.likes.count(),
                             "comments": post.comments.count(),
                             "has_like": has_like}})


@api.route('/post/like/<post_slug>', methods=['PUT'])
def like_post(post_slug):
    author_id = request.json.get("userId", 1)
    # post = Post.query.filter_by(slug=post_slug).with_entities(Post.id, Post.likes, Post.comments).all()
    post = Post.query.filter_by(slug=post_slug).first()

    if Like.query.filter_by(author_id=author_id, post_id=post.id).count() == 0:
        like = Like(author_id=author_id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        return jsonify({"message": "You like this post",
                        "post": {"likes": post.likes.count(),
                                 "comments": post.comments.count()}})
    else:
        return bad_request(message="You already like this post")


@api.route('/post/unlike/<post_slug>', methods=['DELETE'])
def unlike_post(post_slug):
    author_id = request.json.get("userId", 1)
    post = Post.query.filter_by(slug=post_slug).first()
    like = Like.query.filter_by(author_id=author_id, post_id=post.id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "You have unlike this post",
                        "post": {"likes": post.likes.count(),
                                 "comments": post.comments.count()}})
    else:
        return not_found(message="You did not like this post")
