from datetime import datetime
from app import db

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Bug('{self.id}', '{self.title}', '{self.content}', {self.date_created})"