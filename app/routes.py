from flask import render_template, url_for, flash, redirect, request
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

@app.route("/bug/<track_id>")
def bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    return render_template('bug.html', title=bug.title, bug=bug)

@app.route("/bug/<track_id>/update", methods=['GET', 'POST'])
def update_bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    form = TrackerForm()
    if form.validate_on_submit():
        bug.title = form.title.data
        bug.content = form.content.data
        db.session.commit()
        flash('Your bug has been updated!', 'success')
        return redirect(url_for('index', track_id=track_id))
    elif request.method == 'GET':
        form.title.data = bug.title
        form.content.data = bug.content
    return render_template('new_bug.html', title='Update Bug', form=form, legend='Update Bug')

@app.route("/note/<track_id>/delete", methods=['POST'])
def delete_bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    db.session.delete(bug)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('index'))