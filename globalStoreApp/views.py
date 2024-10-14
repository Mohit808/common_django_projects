from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
from globalStoreApp.models import MainCategory,Category, FeatureListModel, Address, Banner
from globalStoreApp.my_serializers import *
from django.db.models import F, FloatField, ExpressionWrapper
import random



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
        search= request.GET.get("search")
        

        if variantId is not None and str(variantId)!="":
            query=Product.objects.filter(variant=variantId)
        else:
            if categoryId  is not None and str(categoryId)!="":
                query=Product.objects.filter(category=categoryId)
            elif search:
                query=Product.objects.filter(name__contains=search)
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
            
            queryDelivery=Order.objects.exclude(status="Delivered").values_list('id', flat=True)
            newList={'delivery':queryDelivery,'featured':response_data}


            return customResponse(message= f'Fetch data successfully', status=200  ,data=newList)
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
    def post(self,request,pk=None):
        productList=request.data.get("product")
        qtyList=request.data.get("qty")
        storeList=request.data.get("store")
        customer=request.data.get("customer")
        address_type=request.data.get("address_type")
        address_title=request.data.get("address_title")
        full_address=request.data.get("full_address")
        house_no=request.data.get("house_no")
        area=request.data.get("area")
        landmark=request.data.get("landmark")
        instruction=request.data.get("instruction")
        latitude=request.data.get("latitude")
        longitude=request.data.get("longitude")
        tip=request.data.get("tip")

        if productList is None or qtyList is None or storeList is None:
            return customResponse(message='product or qty or store is null', status=400,)
        
        if tip is None or not tip:
            tip=0

        order_data = []

        for  x in range(len(productList)):
            order_data.append({
                'product': productList[x],
                'qty': qtyList[x],
                'store': storeList[x]
            })

        created_order_items = [] 

        for item_data in order_data:
            serializer = OrderItemSerializer(data=item_data,)
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
        
        for key, value in finalMap.items():
            print(f"Key: {key}, Value: {value}")
            serializer=CreateOrderSerializer(data={"store":key,"orderItem":str(value).split(","),"otp":random.randint(100000, 999999),"status":"Ordered","customer":customer,"address_type":address_type,"address_title":address_title,"full_address":full_address,"house_no":house_no,"area":area,"landmark":landmark,"instruction":instruction,"latitude":latitude,"longitude":longitude,'tip':tip})
            if serializer.is_valid():
                order = serializer.save() 
            else:
                return customResponse(message='Order Failed to create', status=400, data=serializer.errors)

        return customResponse(message='Order created successfully', status=200, data=itemIds)


class GetOrders(APIView):
    def get(self,request,pk=None):
        querySet=Order.objects.all()
        serializer=OrderSerializer(querySet,many=True,context={'request': request})
        return customResponse(message='Order Fetched sucessfully', status=200, data=serializer.data)


class MyAddress(APIView):
    def post(self,request,pk=None):
        serializer=AddressSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return customResponse(message='Address Saved sucessfully', status=200, data=serializer.data)
        return customResponse(message='Failed to save address', status=2400, data=serializer.errors)
    
    def get(self,request,pk=None):
        query_set=Address.objects.all()
        serializer=AddressSerializer(query_set,many=True)
        return customResponse(message='Address Fetched sucessfully', status=200, data=serializer.data)

class GetBanner(APIView):
    def get(self,request,pk=None):
        query_set=Banner.objects.all()
        serializer=BannerSerializer(query_set,many=True,context={'request': request})
        return customResponse(message='Banner Fetched sucessfully', status=200, data=serializer.data)