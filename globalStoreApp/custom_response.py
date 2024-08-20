# utils.py or similar file
from rest_framework import status
from rest_framework.response import Response

def customResponse(message,status,data=None):
    return Response({
            "message": message,
            "status": status,
            "data": data
        })

def customError(errors):
    # top_errors = {field: str(errors[field][0]) for field in errors}
    first_error_field = next(iter(errors), None)
    if first_error_field:
        first_error_message = errors[first_error_field][0]
    
    return f"{first_error_field} : {first_error_message}"