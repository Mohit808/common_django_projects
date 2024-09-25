from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
from globalStoreApp.models import MainCategory,Category, FeatureListModel
from globalStoreApp.my_serializers import *
from django.db.models import F, FloatField, ExpressionWrapper


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
            querySet = FeatureListModel.objects.all().order_by('-priority')
            response_data = []

            for feature in querySet:
                products = Product.objects.filter(category=feature.category)[:10]
                products_data = ProductSerializer(products, many=True,context={'request': request}).data
                feature_data = {
                    "name": feature.name,
                    "highlight": feature.highlight,
                    "feature_list": products_data
                }
                response_data.append(feature_data)


            return customResponse(message= f'Fetch data successfully', status=200  ,data=response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

class GetHotDeals(APIView):
    def get(self, request,pk=None):
        query = Product.objects.annotate(
            discount_difference=ExpressionWrapper(
                F('price') - F('discountedPrice'),
                output_field=FloatField()
            ),
            discount_percentage=ExpressionWrapper(
                (F('price') - F('discountedPrice')) / F('price') * 100,
                output_field=FloatField()
            )
        ).filter(discountedPrice__isnull=False).order_by('-discount_percentage')
        serializer = ProductSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    

class CreateOrders(APIView):
    def get(self,request,pk=None):
        productList=request.data.get("products")
        qtyList=request.data.get("qty")
        storeList=request.data.get("store")
        print(productList)
        print(qtyList)
        print(storeList)
        # productList= [1,2,3]
        # qtyList= [1,2,3]
        # storeList=[1,2,1]
        
        order_data = []

        for  x in range(len(productList)):
            order_data.append({
                'product': productList[x],
                'qty': qtyList[x],
                'store': storeList[x]
            })

        # print(order_data)
        created_order_items = [] 
        # created_order_items_map = {} 

        for item_data in order_data:
            serializer = OrderItemSerializer(data=item_data)
            if serializer.is_valid():
                order_item = serializer.save() 
                created_order_items.append(order_item)
            else:
                return customResponse(message='Order Failed to create', status=400, data=serializer.errors)
        
        itemIds=[item.id for item in created_order_items]

        finalList=[]
        finalMap={}
        for x in range(len(storeList)):
            if storeList[x] in finalList:
                finalMap[storeList[x]]=f"{finalMap[storeList[x]]},{itemIds[x]}"
            
            else:
                finalList.append(storeList[x])
                finalMap[storeList[x]]=itemIds[x]
        
        # print(finalMap)

        for key, value in finalMap.items():
            print(f"Key: {key}, Value: {value}")
            serializer=OrderSerializer(data={"store":key,"orderItem":str(value).split(","),"otp":"123456","status":"Ordered"})
            if serializer.is_valid():
                order = serializer.save() 
            else:
                return customResponse(message='Order Failed to create', status=400, data=serializer.errors)


        # for x in range(len(storeList)):
        #     serializer=OrderSerializer({"store":storeList[x],"orderItem":created_order_items[x],"otp":"123456","status":"Ordered"})
        #     if serializer.is_valid():
        #         order_item = serializer.save() 
        #     else:
        #         return customResponse(message='Order Failed to create', status=400, data=serializer.errors)


        return customResponse(message='Order created successfully', status=200, data=itemIds)


        