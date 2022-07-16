from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

admin = Admin(app, name='Dashboard')



class Article(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(15), nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.number

admin.add_view(ModelView(Article, db.session))

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request_method == 'POST' and request.form['username'] == 'POST' and "Oleg" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    
    return render_template('login.html', title='Autorisation', menu=menu)


@app.route("/posts")
def posts():

    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', title = "Posts", articles=articles)

@app.route("/posts/<int:number>")
def def_post(number):

    article = Article.query.get(number)
    return render_template('def_post.html', title = "Post", article=article)

@app.route("/posts/<int:number>/edit", methods=['POST', 'GET'])
def def_post_edit(number):
    article = Article.query.get_or_404(number)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        tag = request.form['tag']
        img_url = request.form['img_url']

        try:
            db.session.commit()
            return redirect('/posts/<int:number>')
        except:
            return "!Eroor!"
    else:
        return render_template('edit_post.html', article=article)

@app.route("/posts/<int:number>/delete")
def def_post_delete(number):

    article = Article.query.get_or_404(number)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return '!ERrOr!'

@app.route("/make_post", methods=['POST', 'GET'])
def dbase():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        tag = request.form['tag']
        img_url = request.form['img_url']

        article = Article(title=title, intro=intro, text=text, tag=tag, img_url=img_url)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/make_post')
        except:
            return "!Eroor!"
    else:
        return render_template('make_post.html')



if __name__=="__main__":
    app.run(debug=True)