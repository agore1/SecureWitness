__author__ = 'austin'
import click
import requests
from simplecrypt import encrypt, decrypt

# s = requests.Session()  # Session variable keeps cookies intact for authentication


@click.group()
def login():
    pass
    # click.echo('This is the standalone program.')
    # Program wide system variables for maintaining authentication


@click.group()
@click.pass_context   # This enables passing a session context variable for staying logged in.
def main(ctx):
    """Authenticate with the Secure Witness server."""
    username = click.prompt('Please enter your username', type=str)
    password = click.prompt('Please enter your password', hide_input=True, type=str)
    # click.echo('The username was: {0} and the password was: {1}'.format(username, password))
    s = requests.Session()
    login_response = s.get('http://127.0.0.1:8000/accounts/login/')  # Obtain a csrf cookie
    # Format form data for authentication
    payload = {'password': password, 'username': username, 'csrfmiddlewaretoken': login_response.cookies['csrftoken']}
    r = s.post('http://127.0.0.1:8000/accounts/login/', data=payload)
    # TODO: Check for login success
    click.echo("You are logged in now.")

    # Create a dictionary to store variables to be passed to reports method
    ctx.obj = {}
    ctx.obj['session'] = s
    ctx.obj['username'] = username

@main.command()
@click.pass_context
def reports(ctx):
    """List all reports that are visible to the current user."""
    session = ctx.obj['session']
    # r = session.get('http://127.0.0.1:8000/accounts/' + ctx.obj['username'] + '/reports')
    # click.echo(r.text)
    r = session.get('http://127.0.0.1:8000/standalone/reports/' + ctx.obj['username'] + '/')
    click.echo(r.text)

@main.command()
@click.argument('report_id', default=1, required=True)
@click.pass_context
def view(ctx, report_id):
    """View the details of a report."""
    session = ctx.obj['session']
    r = session.get('http://127.0.0.1:8000/standalone/viewreport/' + ctx.obj['username'] + '/' + str(report_id) + '/')
    click.echo(r.text)


@main.command()
@click.argument('report_id', default=-1, required=True)
@click.argument('file_num', default=-1, required=True)
@click.pass_context
def download(ctx, report_id, file_num):
    """Download the files attached to a report."""
    # Guidance on downloading from http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    if report_id > 0 and file_num > 0:
        local_filename = click.prompt("What would you like to call the file you're downloading?", type=str)
        session = ctx.obj['session']
        url = 'http://127.0.0.1:8000/standalone/download/' + ctx.obj['username'] + '/' + str(report_id) + '/' + str(file_num)
        r = session.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    f.flush()
        click.echo("File downloaded.")
    else:
        click.echo("Please enter valid input for report_id and file_num")



@login.command()
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


@login.command()
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


@login.command()
def listreports():
    """List all reports that are visible to the logged-in user"""
    click.echo(s.cookies)
    # r = s.get('http://127.0.0.1:8000/accounts/profile/')
    # click.echo(r.text)

