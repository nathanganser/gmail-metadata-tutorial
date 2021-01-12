from oauth2client.client import Credentials
from googleapiclient.discovery import build
import json


def create_service():
    # metadata scope
    SCOPES = ['https://www.googleapis.com/auth/gmail.metadata']

    # add your own data to the file
    json_credential_dict = {"token_expiry": None, "user_agent": None, "invalid": False,
                                "client_id": "YOUR_CLIENT_ID",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "client_secret": "YOUR_CLIENT_SECRET", "_module": "oauth2client.client",
                                "_class": "OAuth2Credentials", "scopes": SCOPES,
                                'refresh_token': "REFRESH_TOKEM",
                                'access_token': "ACCESS_TOKEN"}

    cred = Credentials.new_from_json(json.dumps(json_credential_dict))

    service = build("gmail", "v1", credentials=cred, cache_discovery=False)

    # try it!
    message = service.users().messages().list(userId="me").execute()
    mes = message.get('messages')[0]['id']
    if mes:
        print(f'Connection with API established successfully!')
        return service
