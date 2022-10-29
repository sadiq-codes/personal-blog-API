# Personal-blog-API

This is back-end api of my personal blog application build with python and flask as the main dependency.


## Features
- Authentication and Authorization
- JWT middleware for authentication
- File upload to s3
- Database Intergration
- Test
- CRUD for posts, comments, tags, likes, and categories.


## Getting Stated 

``` bash 
git clone https://github.com/bbkrmuhd/personal-blog-API.git

cd personal-blog-API

python3 -m venv env

source env/bin/activate

python3 -m pip install -r requirements.txt

```

# Usage

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

```
