from datetime import datetime
from app import db



class Tracker(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
