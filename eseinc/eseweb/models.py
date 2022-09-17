from email.policy import default
from flask_login import UserMixin
from eseweb import db, login_manager
from datetime import datetime
from eseweb import bcrpt

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True, default='ggghhh123')

    def __repr__(self):
        return f'User(Email: {self.email}, Username: {self.username}, pass: {self.password})'

    @property
    def password_enc(self):
        return self.password_enc

    @password_enc.setter
    def password_enc(self, plain_text_password): 
        self.password = bcrpt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrpt.check_password_hash(self.password, attempted_password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Posts', backref='category', lazy=True)

    def __repr__(self):
        return f'{self.name}'



class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String(20), nullable=False, default=datetime.today().strftime('%Y-%m-%d'))
    post_image = db.Column(db.String(200), nullable=True)
    mins_read = db.Column(db.Integer, nullable=False)
    preview_text = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'Posts(title: {self.title}, categoryid: {self.category_id}, Cat: {self.category})'




class ClientReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(200), nullable=False)
    client_review = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'(Review name: {self.project_name})'



class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.String(600), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    client_review = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'(Review name: {self.project_name})'



class EmailList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'(Email: {self.Email})'



class Faqs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(700), nullable=False)
    answer = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'({self.question})'