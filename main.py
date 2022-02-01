from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/blog')
def get_blog():
    blog_url = "https://api.npoint.io/eef34c0eb71ea8b95cd3"
    response = requests.get(blog_url)
    blog_posts = response.json()
    return render_template("index.html", posts=blog_posts)

@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    blog_url = "https://api.npoint.io/eef34c0eb71ea8b95cd3"
    response = requests.get(blog_url)
    blog_posts = response.json()
    return render_template("post.html", posts=blog_posts, id=blog_id)



if __name__ == "__main__":
    app.run(debug=True)
