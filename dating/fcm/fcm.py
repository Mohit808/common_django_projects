import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests


service_account_file = '/Users/apple/Downloads/myngle-firebase-adminsdk-fbsvc-97a7290361.json'
credentials = service_account.Credentials.from_service_account_file(
    service_account_file,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)



# DEVICE_TOKEN="eeXmsnEpTvmv8qIQAjQvLq:APA91bHGOR6lpYMTgBYEwKoMk7OmwOb3H2w-TMiRJVOgilQeBuvaBPcB9MON8JnAfA8IwVCW4AAu7mn181RXzsEsgHIU_4eqpBfDS6_dWAniCXzEs7qIpAk"

PROJECT_ID = 'myngle' 
url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"


def get_access_token():
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token



def send_fcm_message(device_token, title, body):
    access_token=get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }
    message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            }
        # You can add "data": {...} for custom key-values
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    pass



