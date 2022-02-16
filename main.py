from flask import Flask, render_template
from post import Post
import requests

posts = requests.get("https://api.npoint.io/2c5f72cebe7064305468").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"], post["date"])
    post_objects.append(post_obj)

app = Flask(__name__)


@app.route('/')
def get_home():
    return render_template("index.html", all_posts=post_objects)


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route("/contact")
def get_contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def get_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
