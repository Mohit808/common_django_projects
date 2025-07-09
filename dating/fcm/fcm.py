import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging



def send_push_notification(token, title, body, data=None):

    cred = credentials.Certificate("dating/fcm/myngle-firebase-adminsdk-fbsvc-cef355a83f.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
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




