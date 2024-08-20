from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse


# Create your views here.

def index(request):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo Page</title>
        <style>
            .demo {
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            .demo h1 {
                color: #333;
            }
            .demo p {
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="demo">
            <h1>Welcome to Common Django projects</h1>
            <p>Code Editing and project management made easy</p>
            <p>Access to full source code editing and all functionalities is available in the paid version.</p>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html_content)

