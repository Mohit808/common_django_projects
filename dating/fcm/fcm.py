import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests
import time
from rest_framework.views import APIView
from common_function.custom_response import *
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator


# DEVICE_TOKEN="eeXmsnEpTvmv8qIQAjQvLq:APA91bHGOR6lpYMTgBYEwKoMk7OmwOb3H2w-TMiRJVOgilQeBuvaBPcB9MON8JnAfA8IwVCW4AAu7mn181RXzsEsgHIU_4eqpBfDS6_dWAniCXzEs7qIpAk"

PROJECT_ID = 'myngle' 
url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"


access_token_cache = {
    "token": None,
    "expiry": 0
}

def get_access_token():
    now = time.time()
    if access_token_cache["token"] is None or now >= access_token_cache["expiry"]:
        
        service_account_file = '/Users/apple/Downloads/myngle-firebase-adminsdk-fbsvc-97a7290361.json'
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )


        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        access_token_cache["token"] = credentials.token
        access_token_cache["expiry"] = credentials.expiry.timestamp() - 60  # renew 1 min early
    return access_token_cache["token"]

# def get_access_token():
#     request = google.auth.transport.requests.Request()
#     credentials.refresh(request)
#     return credentials.token



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
    

access_token=get_access_token()


class SendNotification(APIView):
    
    def post(self,request):
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