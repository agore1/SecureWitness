__author__ = 'austin'
import click

@click.group()
def main():
    click.echo('This is the standalone program.')


@main.command()
# @click.option()
def login():
    """Authenticate with the Secure Witness server."""
    username = click.prompt('Please enter your username', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    click.echo('The username was: {0} and the password was: {1}'.format(username, password))
