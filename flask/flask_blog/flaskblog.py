from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# url_for 함수 : static 의 위치를 찾아줌
app = Flask(__name__)
app.config['SECRET_KEY'] = '6026f889a75eae515d0f2f94f4e7d227'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# model
class User(db.Model):
    # primary key 로 지정해두면 auto_increment 적용됨
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Post 모델에 관계 맺음
    # backref : author 컬럼으로 관계 가짐
    # lazy : db에서 데이터 로드할 때 필요한 순간에 실행 (데이터를 가져올것이다)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User({}, {}, {})".format(self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post({}, {})".format(self.title, self.date_posted)


# one-to-many : user-posts


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    # posts에 전달하는 인자 이름(빨간색 글자)으로 템플릿에서 데이터에 접근
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    # 만들어둔 form 을 템플릿에 전달
    form = RegistrationForm()
    # is valid when it submitted
    if form.validate_on_submit():
        # bootstrap 이 지원하는 alert class 중에서 success를 적용하기위해 2번째 인자로 전달
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # 만들어둔 form 을 템플릿에 전달
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)