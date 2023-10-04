# Personal-blog-API

This is back-end api of my personal blog application build with python and flask as the main dependency.


## Features
- Authentication and Authorization
- JWT middleware for authentication
- File upload to s3
- Database Intergration
- Test
- CRUD for posts, comments, tags, likes, and categories.


## Installation 

``` bash 
git clone https://github.com/bbkrmuhd/personal-blog-API.git

cd personal-blog-API

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r requirements.txt

```

## Usage

This project requires environmental variables for runtime configuration.

```bash
export FLASK_APP=blog.py

# If debug equals to true

export FLASK_DEBUG=1 #set this to 0 in production

export FLASK_CONFIG=development  # export FLASK_CONFIG=production for production environment

# Setup Flask-Migrate 

flask db init && flask db migrate && flask db upgrade

# To create flask admin

export BLOG_ADMIN=fake@gmail.com
export BLOG_PASSWORD=fake
export BLOG_USERNAME=fake
export IS_BLOG_ADMIN=True

# run the following

flask createsuperuser

# run server

flask run

```

# Api Endpoints

- `api.create_category       POST       /api/v1/create/category`
- `api.create_comment        POST       /api/v1/comment/create/<post_slug>`
- `api.create_post           POST       /api/v1/post/create`
- `api.create_tag            POST       /api/v1/create/tag`
- `api.delete_category       DELETE     /api/v1/category/delete/<category_slug>`
- `api.delete_comment        DELETE     /api/v1/comment/delete/<comment_id>`
- `api.delete_post           DELETE     /api/v1/post/delete/<post_slug>`
- `api.delete_post_tag       DELETE     /api/v1/tag/remove/<post_slug>/<tag_slug>`
- `api.delete_tag            DELETE     /api/v1/tag/delete/<tag_slug>`
- `api.featured              GET        /api/v1/posts/featured`
- `api.get_category          GET        /api/v1/category/list`
- `api.get_comments          GET        /api/v1/comments/get/<post_slug>`
- `api.get_comments_likes    GET        /api/v1/get/comments/likes/<post_slug>`
- `api.get_post_by_category  GET        /api/v1/category/<category_slug>`
- `api.get_post_by_tags      GET        /api/v1/tags/<tag_slug>`
- `api.like_post             PUT        /api/v1/post/like/<post_slug>`
- `api.post_detail           GET        /api/v1/post/detail/<post_slug>`
- `api.post_list             GET        /api/v1/posts/list`
- `api.profile               GET        /api/v1/profile/<int:user_id>`
- `api.unlike_post           DELETE     /api/v1/post/unlike/<post_slug>`
- `api.update_category       PUT        /api/v1/category/update/<category_slug>`
- `api.update_comment        PUT        /api/v1/comment/update/<comment_id>`
- `api.update_post           PUT        /api/v1/post/update/<post_slug>`
- `api.update_tag            PUT        /api/v1/tag/update/<tag_slug>`
- `api.updated_posts         GET        /api/v1/posts/updated`
- `api.user_login            POST       /api/v1/login`
- `api.user_logout           GET        /api/v1/logout`
- `api.user_signup           GET, POST  /api/v1/signup`


# License
MIT

