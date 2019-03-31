import click
from app import app, db
from app.models import User, Thing


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    print("Initialized database.")


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--email', prompt=True, help='The email used to Identity.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, email, password):
    db.create_all()
    user = User.query.first()
    if user:
        print("Updating user...")
        user.name = username
        user.email = email
        user.generate_password_hash(password)
    else:
        print("Creating user...")
        user = User(name="hippieZhou")
        user.email = email
        user.generate_password_hash(password)
        db.session.add(user)
    db.session.commit()
    print('Done.')
