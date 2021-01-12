import os
from oauth2client import client


def create_gmail_data(auth_code):
    print('getting the credentials files')

    CLIENT_SECRET_FILE = "your_client_secret.json"

    # Exchange auth code for access token & refresh token

    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/gmail.metadata', 'profile',
         'email'],
        auth_code)

    # Get profile info from token
    print('got the data from Google')
    refresh_token = credentials.refresh_token
    access_token = credentials.access_token
    email = credentials.id_token['email']
    name = credentials.id_token['name']
