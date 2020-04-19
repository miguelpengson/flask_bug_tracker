from datetime import datetime
from flask import render_template, flash, redirect, url_for, requests, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import TrackerForm
from app.models import User, Tracker
from app.main import bp


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    track = Tracker.query.all()
    return render_template('index.html', track=track)


@app.route("/bug/new", methods=['GET', 'POST'])
@login_required
def new_bug():
    form = TrackerForm()
    if form.validate_on_submit():
        track = Tracker(project=form.project.data, subject=form.subject.data, content=form.content.data, 
                        priority=form.priority.data, progress=form.progress.data, author=current_user)
        db.session.add(track)
        db.session.commit()
        flash('Your new issue is being tracked!', 'success')
        return redirect(url_for('index'))
    return render_template('new_bug.html', title='New Bug Report', form=form, legend='New Bug')

@app.route("/bug/<int:track_id>")
def bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    return render_template('bug.html', title=bug.subject, bug=bug)

@app.route("/bug/<int:track_id>/update", methods=['GET', 'POST'])
def update_bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    if bug.author != current_user:
        abort(403)
    form = TrackerForm()
    if form.validate_on_submit():
        bug.project = form.project.data
        bug.subject = form.subject.data
        bug.content = form.content.data
        bug.priority = form.priority.data
        bug.progress = form.progress.data
        db.session.commit()
        flash('Your bug has been updated!', 'success')
        return redirect(url_for('index', track_id=track_id))
    elif request.method == 'GET':
        form.project.data = bug.project
        form.subject.data = bug.subject
        form.content.data = bug.content
        form.priority.data = bug.priority
        form.progress.data = bug.progress
    return render_template('new_bug.html', title='Update Bug', form=form, legend='Update Bug')

@app.route("/note/<int:track_id>/delete", methods=['POST']) # note? must be bug?
def delete_bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    if bug.author != current_user:
        abort(403)
    db.session.delete(bug)
    db.session.commit()
    flash('Your bug topic has been deleted!', 'success')
    return redirect(url_for('index'))