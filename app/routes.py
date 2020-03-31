from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Tracker
from app.forms import LoginForm, TrackerForm, RegistrationForm

@app.route("/")
@app.route("/index")
@login_required
def index():
    track = Tracker.query.all()
    return render_template('index.html', track=track)

# Logging users in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Logging users out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # ????
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User profile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route("/bug/new", methods=['GET', 'POST'])
@login_required
def new_bug():
    form = TrackerForm()
    if form.validate_on_submit():
        track = Tracker(subject=form.subject.data, content=form.content.data, 
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
        bug.subject = form.subject.data
        bug.content = form.content.data
        bug.priority = form.priority.data
        db.session.commit()
        flash('Your bug has been updated!', 'success')
        return redirect(url_for('index', track_id=track_id))
    elif request.method == 'GET':
        form.subject.data = bug.subject
        form.content.data = bug.content
    return render_template('new_bug.html', title='Update Bug', form=form, legend='Update Bug')

@app.route("/note/<int:track_id>/delete", methods=['POST'])
def delete_bug(track_id):
    bug = Tracker.query.get_or_404(track_id)
    if bug.author != current_user:
        abort(403)
    db.session.delete(bug)
    db.session.commit()
    flash('Your bug topic has been deleted!', 'success')
    return redirect(url_for('index'))