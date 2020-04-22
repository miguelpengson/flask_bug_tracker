from app import create_app, db
from app.models import User, Tracker

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Tracker': Tracker}


if __name__ == '__main__':
    app.run(debug=True)
