from flask import render_template, url_for, flash, redirect
from app import app, db
from app.models import Tracker
from app.forms import TrackerForm

@app.route("/")
@app.route("/index")
def index():
    tracker = Tracker.query.all()
    return render_template('index.html', tracker=tracker)


@app.route("/bug/new", methods=['GET', 'POST'])
def new_bug():
    form = TrackerForm()
    return render_template('new_bug.html', title='New Bug Report', form=form, legend='New Bug')
