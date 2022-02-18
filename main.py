from flask import Flask, render_template, request
from post import Post
import os
import smtplib
import requests

FROM_EMAIL = os.environ.get("FROM_EMAIL")
FROM_PASSWORD = os.environ.get("FROM_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

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


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == 'POST':
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phoneNumber"]
        message = request.form["message"]
        content = f"Name: {name}\n" \
                  f"Email: {email}\n" \
                  f"Phone Number: {phone}\n" \
                  f"Message: {message}"

        print(FROM_EMAIL, FROM_PASSWORD)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=FROM_PASSWORD)

            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject:New Message!\n\n{content}"
            )
        return render_template("form-entry.html")
    else:
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
