
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    pass


@click.command('init-db', help='Initialized the database')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
