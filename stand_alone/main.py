__author__ = 'austin'
import click
import requests
from simplecrypt import encrypt, decrypt

@click.group()
def main():
    click.echo('This is the standalone program.')


@main.command()
def login():
    """Authenticate with the Secure Witness server."""
    username = click.prompt('Please enter your username', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    click.echo('The username was: {0} and the password was: {1}'.format(username, password))

    s = requests.Session()
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    r = s.get("http://httpbin.org/cookies")
    click.echo(r.text)
    # response = urllib.request.urlopen('http://127.0.0.1:8000/standalone/')
    # html = response.read()
    # click.echo(html)

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
    """Debug only: encrypt a file."""
    filename = click.prompt('Please enter the filename to be encrypted', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    # Open the file and encrypt it
    with open(filename, 'rb')as unencrypted:
        ciphertext_bytes = encrypt(password, unencrypted.read())
        # Write the encrypted data to a new file
        with open(filename + '.enc', 'wb') as encrypted:
            encrypted.write(ciphertext_bytes)
    click.echo('Finished encrypting out file.')




