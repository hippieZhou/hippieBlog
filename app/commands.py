
import click
from app import db
from app.models import User
from flask import current_app, g
from flask.cli import with_appcontext


def init_admin(name, email, pwd):
    User.query.filter(User.name == name).delete()
    db.session.commit()

    user = User(name=name, email=email, pwd=pwd)
    user.generate_password_hash(user.pwd)
    db.session.add(user)
    db.session.commit()
    print('done...')


@click.command('init-admin', help='Initialized the admin')
@click.option('--name', prompt=True, default='admin')
@click.option('--email', prompt=True, default='admin@outlook.com')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def init_admin_command(name, email, password):
    init_admin(name, email, password)
    click.echo('Initialized the database.')
