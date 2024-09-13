from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
from globalStoreApp.models import MainCategory,Category, FeatureListModel
from globalStoreApp.my_serializers import *


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




class GetMainCategories(APIView):
    def get(self, request,pk=None):
        
        query=MainCategory.objects.all()

        serializer = MainCategorySerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    
    
class GetProducts(APIView):
    def get(self, request,pk=None):
        variantId= request.GET.get("variantId")
        categoryId= request.GET.get("categoryId")
        if variantId is not None and str(variantId)!="":
            query=Product.objects.filter(variant=variantId)
        else:
            if categoryId  is not None and str(categoryId)!="":
                query=Product.objects.filter(category=categoryId)
            else:
                query=Product.objects.all()

        serializer = ProductSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    

class GetVariants(APIView):
    def get(self, request,pk=None):

        query=Variant.objects.filter(category=pk)

        serializer = VariantSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    
    

class GetDashboard(APIView):
    def get(self, request,pk=None):

        try:
            feature_list_models = FeatureListModel.objects.all()

            distinct_categories = Category.objects.filter(featurelistmodel__in=feature_list_models).distinct()

            response_data = []

            for category in distinct_categories:
                products = Product.objects.filter(category=category)[:10]
                products_data = ProductSerializer(products, many=True).data
                category_data = CategorySerializer(category).data
                category_data['products'] = products_data
                response_data.append(category_data)
            
            return customResponse(message= f'Fetch data successfully', status=200  ,data=response_data)
            # return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    