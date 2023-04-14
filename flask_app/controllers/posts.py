from flask_app import app
from flask import redirect,session,render_template,request,flash
from flask_app.models.post import Post
from flask_app.controllers import users
from flask_bcrypt import Bcrypt

@app.route('/create/post', methods=['POST'])
def create_post():
    print(len(request.form['content']))
    if len(request.form['content']) < 1:
        flash('Post cannot be empty',  'post')
        return redirect('/wall')
    Post.create_post(request.form)
    return redirect('/wall')

@app.route('/delete/post/<int:id>')
def delete_post(id):
    data = { 'id': id }
    Post.delete_post(data)
    return redirect('/wall')