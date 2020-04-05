from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(128))
    trackers = db.relationship('Tracker', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}, '{self.last_seen}')"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    priority = db.Column(db.String(16), nullable=False)
    progress = db.Column(db.String(16), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Bug('{self.id}', '{self.subject}', '{self.content}', '{self.priority}', '{self.progress}', '{self.date_created}')"