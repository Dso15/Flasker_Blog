from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime



# Create SQLAlchemy object
db = SQLAlchemy()


# -------------------- Login Manager --------------------
login_manager = LoginManager()
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# -------------------- End of Login Manager --------------------


# -------------------- Post Model --------------------
class Post(db.Model):
    """
    Post Model Get:
    ---------------
    title = The title of the post \n
    author = Author of the post \n
    content = Post contet \n 
    slug = post slug

    _date_posted = set automaticlly.
    """
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.Integer, db.ForeignKey('slug.id'))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('UserMessage', backref='message')
# -------------------- End of Post Model --------------------


# -------------------- User Model --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    confirm = db.Column(db.Boolean, default=False, nullable=False)
    confirm_at = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    posts = db.relationship('Post', backref='poster')
    messages = db.relationship('UserMessage', backref='user_message')

    # Revoke access to password variable
    @property
    def password(self):
        raise AttributeError('Password is not reachable!!')
    
    # Set setter for hashing user password
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Varify user password 
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Create reset token
    def get_token(self, salt):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=salt)
        return serializer.dumps(self.id, salt=salt) 
    
    # Verify reset token
    @staticmethod
    def verify_token(token, salt, expires_sec=1800):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=salt)
        try:
            user_id = serializer.loads(token, max_age=expires_sec)
        except:
            return None
        return User.query.get_or_404(user_id)
# -------------------- End of User Model --------------------


# -------------------- Slug Model --------------------
class Slug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))       
    posts = db.relationship('Post', backref='category')
# -------------------- End of Slug Model --------------------


# -------------------- Message Model --------------------
class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))       
    date_posted = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# -------------------- End of Message Model --------------------