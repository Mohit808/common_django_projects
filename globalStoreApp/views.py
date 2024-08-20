from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def index(request):
    # return  JsonResponse(data={"message": "Hello World"})
    return render(render, html)



html= """ 
<div class="demo">
  <h1>Demo</h1>
  <p>This is a demo html page. You can edit the HTML, SCSS and see the changes in real time.</p>
  <p>Access to full source code editing and all functionalities is available in the paid version.</p>
</div>
"""
