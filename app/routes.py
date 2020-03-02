from flask import render_template, url_for
from app import app, db
from app.models import Tracker
from app.forms import TrackerForm

@app.route('/')
@app.route('/index')
def index():
    track = Tracker.query.order_by(Tracker.date_created).all()
    form = TrackerForm()
    return render_template('index.html', track=track, form=form)

   