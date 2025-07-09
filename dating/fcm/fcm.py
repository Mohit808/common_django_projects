


# import json
# import google.auth
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# import requests
# from rest_framework.views import APIView
# from common_function.custom_response import *

# # Path to your service account key
# SERVICE_ACCOUNT_FILE = "dating/fcm/myngle-firebase-adminsdk-fbsvc-cef355a83f.json"

# # Define the FCM endpoint
# PROJECT_ID = "myngle"
# FCM_URL = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

# def get_access_token():
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE,
#         scopes=["https://www.googleapis.com/auth/firebase.messaging"]
#     )
#     credentials.refresh(Request())
#     return credentials.token

# print("Access Token:", get_access_token())

# # def send_fcm_v1(token, title, body, data=None):
    
# #     access_token = get_access_token()


# #     headers = {
# #         "Authorization": f"Bearer {access_token}",
# #         "Content-Type": "application/json; UTF-8",
# #     }

# #     message = {
# #         "message": {
# #             "token": token,
# #             "notification": {
# #                 "title": title,
# #                 "body": body
# #             },
# #             "data": data or {}
# #         }
# #     }

# #     response = requests.post(FCM_URL, headers=headers, data=json.dumps(message))

# #     print("Status Code:", response.status_code)
# #     print("Response:", response.text)

# # # Example usage


# class SendData(APIView):
#     def get(self, request,pk=None):
#        get_access_token()
#        return customResponse(data="Hello",message= f'Fetch data successfully', status=200)




# # import firebase_admin
# # from firebase_admin import credentials
# # from firebase_admin import messaging



# # def send_push_notification(token, title, body, data=None):

# #     cred = credentials.Certificate("dating/fcm/myngle-firebase-adminsdk-fbsvc-cef355a83f.json")
# #     if not firebase_admin._apps:
# #         firebase_admin.initialize_app(cred)

# #     message = messaging.Message(
# #         notification=messaging.Notification(
# #             title=title,
# #             body=body,
# #         ),
# #         token=token,
# #         data=data or {},
# #     )

# #     # response = messaging.send(message)
# #     # print("Successfully sent message:", response)



# # send_push_notification("eeXmsnEpTvmv8qIQAjQvLq:APA91bHGOR6lpYMTgBYEwKoMk7OmwOb3H2w-TMiRJVOgilQeBuvaBPcB9MON8JnAfA8IwVCW4AAu7mn181RXzsEsgHIU_4eqpBfDS6_dWAniCXzEs7qIpAk", "Test Title", "Test Body", {"key": "value"})




