from flask import render_template, url_for, flash, redirect
from app import app, db
from app.models import Tracker
from app.forms import TrackerForm

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Tracker': Tracker}

@app.route("/")
@app.route("/index")
def index():
    track = Tracker.query.all()
    return render_template('index.html', track=track)


@app.route("/bug/new", methods=['GET', 'POST'])
def new_bug():
    form = TrackerForm()
    if form.validate_on_submit():
        track = Tracker(title=form.title.data, content=form.content.data)
        db.session.add(track)
        db.session.commit()
        flash('Your Bug tracker has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('new_bug.html', title='New Bug Report', form=form, legend='New Bug')


