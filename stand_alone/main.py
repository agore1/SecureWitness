__author__ = 'austin'
import click
import urllib.request
import urllib.parse

@click.group()
def main():
    click.echo('This is the standalone program.')


@main.command()
def login():
    """Authenticate with the Secure Witness server."""
    username = click.prompt('Please enter your username', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    click.echo('The username was: {0} and the password was: {1}'.format(username, password))

    response = urllib.request.urlopen('http://127.0.0.1:8000/standalone/')
    html = response.read()
    click.echo(html)
