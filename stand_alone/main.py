__author__ = 'austin'
import click
import requests
from simplecrypt import encrypt, decrypt

s = requests.Session()  # Session variable keeps cookies intact for authentication


@click.group()
def main():
    pass
    # click.echo('This is the standalone program.')
    # Program wide system variables for maintaining authentication




@main.command()
def login():
    """Authenticate with the Secure Witness server."""
    username = click.prompt('Please enter your username', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    # click.echo('The username was: {0} and the password was: {1}'.format(username, password))

    login_response = s.get('http://127.0.0.1:8000/accounts/login/')  # Obtain a csrf cookie
    # click.echo(login_response.text)
    # click.echo('\n The login cookie was: \n')
    # click.echo(login_response.cookies['csrftoken'])
    # Format form data for authentication
    payload = {'password': password, 'username': username, 'csrfmiddlewaretoken': login_response.cookies['csrftoken']}
    r = s.post('http://127.0.0.1:8000/accounts/login/', data=payload)
    # r = s.get('http://127.0.0.1:8000/accounts/profile/')
    # TODO: Check for login success
    click.echo(r.text)
    click.echo("You are logged in now.")
    click.echo(s.cookies)


@main.command()
def dec():
    """Decrypt an encrypted file."""
    filename = click.prompt('Please enter the filename to decrypt', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    # Open the encrypted file and decrypt the contents
    with open(filename, 'rb') as encrypted:
        plaintext_bytes = decrypt(password, encrypted.read())
        # Write the decrypted contents to a new file
        with open(filename + '.dec', 'wb') as decrypted:
            decrypted.write(plaintext_bytes)
    click.echo('Finished decrypting the file.')


@main.command()
def enc():
    """Encrypt a file."""
    filename = click.prompt('Please enter the filename to be encrypted', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    # Open the file and encrypt it
    with open(filename, 'rb')as unencrypted:
        ciphertext_bytes = encrypt(password, unencrypted.read())
        # Write the encrypted data to a new file
        with open(filename + '.enc', 'wb') as encrypted:
            encrypted.write(ciphertext_bytes)
    click.echo('Finished encrypting out file.')


@main.command()
def listreports():
    """List all reports that are visible to the logged-in user"""
    click.echo(s.cookies)
    # r = s.get('http://127.0.0.1:8000/accounts/profile/')
    # click.echo(r.text)

