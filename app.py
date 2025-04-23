# app.py

from flask import Flask, render_template, redirect, request
from flask import flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhh"

connect_db(app)

with app.app_context():
    db.create_all()

# New homepage

@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)

@app.route('/users')
def list_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("index.html", users=users)

@app.route('/users/new')
def new_user_form():
    return render_template("new.html")

@app.route('/users/new', methods=["POST"])
def create_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or "https://via.placeholder.com/150"
    )

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("show.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or "https://via.placeholder.com/150"

    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# Post routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user
    )
    db.session.add(new_post)
    db.session.commit()
    # The notification thing hopefully
    flash("Post created successfully!", "success")
    return redirect(f"/users/{user_id}")



@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_show.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_edit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

