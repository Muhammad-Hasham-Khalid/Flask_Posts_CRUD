from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
  _id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(200))
  title = db.Column(db.String(200))
  content = db.Column(db.String(200))

  def __init__(self, author, title, content):
    self.author = author
    self.title = title
    self.content = content

@app.route("/")
def index():
  posts = Post.query.all()
  return render_template("index.html", posts=posts)

@app.route("/new", methods=['POST', 'GET'])
def new():
  if request.method == 'POST':
    author = request.form.get('author').capitalize()
    title = request.form.get('title').capitalize()
    content = request.form.get('content')
    if not author.strip() or not title.strip() or content.strip():
      return redirect("/")
    else:
      new_post = Post(author, title, content)
      db.session.add(new_post)
      db.session.commit()
      return redirect("/")

  return render_template('new.html')

@app.route("/posts/<int:id>")
def view(id):
  try:
    post = Post.query.filter_by(_id=id).first()
  except Exception as e:
    print(e)
  else:
    if not post:
      return redirect("/")
    else:
      return render_template("post.html", post=post)

@app.route("/delete/<int:id>")
def deletePost(id):
  try:
    post = Post.query.filter_by(_id=id).first()
    db.session.delete(post)
    db.session.commit()
  except Exception as e:
    print(e)
  finally:
    return redirect("/")

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)