import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests
import time
from rest_framework.views import APIView
from common_function.custom_response import *
import os

PROJECT_ID = 'common-flutter-apps' 
url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"


access_token_cache = {
    "token": None,
    "expiry": 0
}

def get_access_token():
    now = time.time()
    if access_token_cache["token"] is None or now >= access_token_cache["expiry"]:
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        service_account_file = os.path.join(BASE_DIR, 'fcm', 'globalStoreApp/fcm/common-flutter-apps-firebase-adminsdk-ryx6j-f00bbaac4a.json')

        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )


        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        access_token_cache["token"] = credentials.token
        access_token_cache["expiry"] = credentials.expiry.timestamp() - 60  # renew 1 min early
    return access_token_cache["token"]


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
            },
            "data": {
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    


class SendNotificationQuick(APIView):

    def post(self,request):
        access_token=get_access_token()
        device_token=request.data.get("device_token")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; UTF-8",
        }
        message = {
            "message": {
                "token": device_token,
                "notification": {
                    "title": "title",
                    "body": "body"
                },
                "data": {
                    "title": "title",
                    "body": "body"
                }
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(message))
            print("Status Code:", response.status_code)
            print("Response:", response.text)

            return customResponse(data=f"Status code : {response.status_code} , response : {response.text}",message= f'Notification send successfully', status=200)
        except requests.exceptions.RequestException as e:
            print(f"Error sending FCM message: {e}")
            return customResponse(message=f"Error sending FCM message: {e}", status=500)