from http import HTTPStatus

from pydantic import ValidationError
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from .validators import (
    PostValidator,
    CommentValidator,
)
from .models import (
    db,
    Post,
    Comment,
    User,
)

PAGE = "page"
PER_PAGE = "per_page"
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10

posts = Blueprint("posts", __name__)


@posts.route("/post/<int:post_id>", methods=["GET"])
@login_required
def get_post(post_id):
    post = Post.query.get_or_404(post_id)

    return jsonify({
        "post_id": post.post_id,
        "title": post.title,
        "content": post.content,
        "author": post.author.username,
        "created_at": post.created_at.isoformat(),
    })


@posts.route("/post/<int:post_id>/comment", methods=["GET"])
@login_required
def get_comments_for_post(post_id):
    post = Post.query.get_or_404(post_id)

    page = request.args.get(PAGE, DEFAULT_PAGE, type=int)
    per_page = request.args.get(PER_PAGE, DEFAULT_PER_PAGE, type=int)

    paginated_comments = post.comments.paginate(page=page, per_page=per_page)

    return jsonify({
        "has_next": paginated_comments.has_next,
        "next_page": paginated_comments.next_num,
        "data": [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "author": comment.author.username,
                "created_at": comment.created_at.isoformat(),
            }
            for comment in paginated_comments
        ],
    })


@posts.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment_for_post(post_id):
    try:
        comment_input = CommentValidator.parse_raw(request.data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    post = Post.query.get_or_404(post_id)
    new_comment = Comment(
        content=comment_input.content,
        author_id=current_user.user_id,
        post_id=post.post_id,
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "comment_id": new_comment.comment_id,
        "message": "Comment added",
    }), HTTPStatus.CREATED


@posts.route("/post", methods=["GET"])
@login_required
def get_post_list():
    page = request.args.get(PAGE, DEFAULT_PAGE, type=int)
    per_page = request.args.get(PER_PAGE, DEFAULT_PER_PAGE, type=int)

    paginated_posts = Post.query.paginate(page=page, per_page=per_page)

    return jsonify({
        "has_next": paginated_posts.has_next,
        "next_page": paginated_posts.next_num,
        "data": [
            {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "author": post.author.username,
                "created_at": post.created_at.isoformat(),
            }
            for post in paginated_posts
        ],
    })


@posts.route("/post", methods=["POST"])
@login_required
def add_post():
    try:
        post_input = PostValidator.parse_raw(request.data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    new_post = Post(
        title=post_input.title,
        content=post_input.content,
        author_id=current_user.user_id,
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "post_id": new_post.post_id,
        "message": "New post added",
    }), HTTPStatus.CREATED


@posts.route("/author/<int:author_id>/post", methods=["GET"])
@login_required
def get_posts_by_author(author_id):
    page = request.args.get(PAGE, DEFAULT_PAGE, type=int)
    per_page = request.args.get(PER_PAGE, DEFAULT_PER_PAGE, type=int)

    author = User.query.get_or_404(author_id)
    paginated_authors_posts = author.posts.paginate(
        page=page,
        per_page=per_page,
    )

    return jsonify({
        "has_next": paginated_authors_posts.has_next,
        "next_page": paginated_authors_posts.next_num,
        "data": [
            {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
            }
            for post in paginated_authors_posts
        ],
    })


@posts.route("/author/<int:author_id>/comment", methods=["GET"])
@login_required
def get_comments_by_author(author_id):
    page = request.args.get(PAGE, DEFAULT_PAGE, type=int)
    per_page = request.args.get(PER_PAGE, DEFAULT_PER_PAGE, type=int)

    author = User.query.get_or_404(author_id)
    paginated_authors_comments = author.comments.paginate(
        page=page,
        per_page=per_page,
    )

    return jsonify({
        "has_next": paginated_authors_comments.has_next,
        "next_page": paginated_authors_comments.next_num,
        "data": [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "created_at": comment.created_at.isoformat(),
            }
            for comment in paginated_authors_comments
        ],
    })
