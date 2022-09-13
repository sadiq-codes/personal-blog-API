from flask import request, redirect
from . import api


@api.route('/login/', methods=['GET', 'POST'])
def user_login():
    pass
