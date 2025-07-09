import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("dating/fcm/myngle-firebase-adminsdk-fbsvc-cef355a83f.json")
firebase_admin.initialize_app(cred)



def send_push_notification(token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {},
    )

    response = messaging.send(message)
    print("Successfully sent message:", response)




