from django.shortcuts import render
from common_function.custom_response import *
from rest_framework.views import APIView
from social_network.models import *
from social_network.serializers import *
from rest_framework.pagination import PageNumberPagination
# Create your views here.

def hello(request):
    return customResponse(status=200,message="Successfull")

class Hello(APIView):
    def get(self, request,pk=None):
        query_set=Post.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(query_set, request)
        serializer=PostSerializer(paginated_queryset,many=True)
        # return paginator.get_paginated_response(serializer.data)
        return customResponse(data=serializer.data,message= f'Fetch data successfully', status=200)
    


class PostView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                post = Post.objects.get(id=pk)
                serializer = PostSerializer(post)
                return customResponse(data=serializer.data, message='Post fetched successfully', status=200)
            except Post.DoesNotExist:
                return customResponse(message='Post not found', status=404)
        else:
            query_set = Post.objects.all().order_by('-id')
            paginator = PageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(query_set, request)
            serializer = PostSerializer(paginated_queryset, many=True)
            return customResponse(data=serializer.data, message='Posts fetched successfully', status=200)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return customResponse(data=serializer.data, message='Post created successfully', status=201)
        return customResponse(message='Invalid data', status=400, errors=serializer.errors)