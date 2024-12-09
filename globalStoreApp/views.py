from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
from globalStoreApp.models import MainCategory,Category, FeatureListModel, Address, Banner
from globalStoreApp.my_serializers import *
from django.db.models import F, FloatField, ExpressionWrapper
import random
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated



# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import Point




# class GetNearByAddress(APIView):
#     def get(self, request, pk=None):
#         try:
#             # Get the latitude and longitude from the request query parameters
#             user_lat = float(request.query_params.get('latitude'))
#             user_lon = float(request.query_params.get('longitude'))
#             radius = float(request.query_params.get('radius', 50))  # Optional radius (default: 50 km)

#             # Create a point from the user's location
#             user_location = Point(user_lon, user_lat, srid=4326)

#             # Filter variants by category and proximity using the distance function

#             query = Address.objects.filter(
#                 category=pk,
#                 location__distance_lte=(user_location, radius * 1000)  # radius in meters
#             ).annotate(
#                 distance=Distance('location', user_location)
#             ).order_by('distance')  # Orders by proximity

#             # query = Variant.objects.filter(
#             #     category=pk,
#             #     location__distance_lte=(user_location, radius * 1000)  # radius in meters
#             # ).annotate(
#             #     distance=Distance('location', user_location)
#             # ).order_by('distance')  # Orders by proximity

#             # Serialize the filtered variants
#             serializer = VariantSerializer(query, many=True, context={'request': request})

#             return customResponse(message='Fetch data successfully', status=200, data=serializer.data)
#         except ValueError:
#             return customResponse(message='Invalid latitude or longitude', status=400)
        

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
        brandId=request.GET.get("brandId")

        if brandId:
            query_set=Product.objects.filter(brand=brandId)
            serializer=ProductSerializer(query_set,many=True,context={'request': request})
            return customResponse(message="Product fetched successfully",status=200,data=serializer.data)

        

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
    
    def delete(self, request,pk=None):
        productId= request.GET.get("productId")
        if not productId:
            return customResponse(message="required productId",status=400)
        Product.objects.filter(id=productId).delete()
        return customResponse(message="Product deleted successfully",status=200)

    

class GetVariants(APIView):
    def get(self, request,pk=None):

        query=Variant.objects.filter(category=pk)

        serializer = VariantSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    
    
@authentication_classes([TokenAuthentication])
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
            print(request.user.id)
            queryDelivery=Order.objects.filter(customer_id=request.user.id).exclude(status="Delivered").values_list('id', flat=True)
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
    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateOrders(APIView):
    def post(self,request,pk=None):
        productList=request.data.get("product")
        qtyList=request.data.get("qty")
        storeList=request.data.get("store")
        # customer=request.data.get("customer")
        customer=request.user.id
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



@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetOrders(APIView):
    def get(self,request,pk=None):
        querySet=Order.objects.filter(customer=request.user.id)
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
    def get(self,request):
        storeId=request.GET.get("storeId")
        if storeId:
            query_set=Banner.objects.filter(store=storeId).order_by('-priority')
        else:
            query_set=Banner.objects.all()
        
        serializer=BannerSerializer(query_set,many=True,context={'request': request})
        return customResponse(message='Banner Fetched sucessfully', status=200, data=serializer.data)
    
class GetStore(APIView):
    def get(self,request,pk=None):
        query_set=Store.objects.all()
        serializer=StoreSerializer(query_set,many=True)
        return customResponse(message="Store fetched successfully",status=200,data=serializer.data)
    

class GetUniqueCategoryByStore(APIView):
    def get(self,request,pk=None):
        storeId=request.GET.get("storeId")
        if storeId:
            unique_category_ids = Product.objects.filter(store_id=storeId).values('category').distinct()
            unique_categories = Category.objects.filter(id__in=unique_category_ids)
            serializer = CategorySerializer(unique_categories, many=True,context={'request': request})
            return customResponse(message="Categories fetched successfully",status=200,data=serializer.data)
        else:
            return customResponse(message="StoreId is null",status=400)

class GetCategory(APIView):
    def get(self,request,pk=None):
        unique_categories = Category.objects.filter(main_category=pk)
        serializer = CategorySerializer(unique_categories, many=True,context={'request': request})
        return customResponse(message="Categories fetched successfully",status=200,data=serializer.data)
        

class GetBrands(APIView):
    def get(self,request,pk=None):
        query_set=Brand.objects.all()
        serializer=BrandSerializer(query_set,many=True,context={'request': request})
        return customResponse(message="Brand fetched successfully",status=200,data=serializer.data)

class GetFestivalOffer(APIView):
    def get(self,request,pk=None):
        query_set=FestivalOffer.objects.filter(priority=10).first()
        serializer=FestivalOfferSerializer(query_set,context={'request': request})
        return customResponse(message="Fetsival Offers fetched successfully",status=200,data=serializer.data)


class GetVariantByFestival(APIView):
    def get(self,request,pk=None):
        festivalId=request.GET.get("festivalId")
        if festivalId:
            unique_variant_ids = FestivalOffer.objects.filter(id=festivalId).values('variant')
            unique_variants = Variant.objects.filter(id__in=unique_variant_ids)
            serializer = VariantSerializer(unique_variants, many=True,context={'request': request})
            return customResponse(message="Variants fetched successfully",status=200,data=serializer.data)
        else:
            return customResponse(message="festivalId is null",status=400)
        
@authentication_classes([TokenAuthentication])
class GetDeliveryOrders(APIView):
    def get(self,request,pk=None):
        order_queryset = Order.objects.exclude(deliveryPartner=request.user.id)
        serializer = DeliveryOderSerializer(order_queryset, many=True,context={'request': request})
        return customResponse(message="Orders fetched successfully",status=200,data=serializer.data)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetMyDeliveryOrders(APIView):
    def get(self,request,pk=None):
        order_queryset = Order.objects.filter(deliveryPartner_id=request.user.id)
        serializer = DeliveryOderSerializer(order_queryset, many=True,context={'request': request})
        return customResponse(message="Orders fetched successfully",status=200,data=serializer.data)
    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class AcceptOrders(APIView):
    def post(self,request,pk=None):
        order_id=request.data.get("order_id")
        status=request.data.get("status")
        if not order_id:
            return customResponse(message="order_id required",status=400)
        status=request.data.get("status")
        if not status:
            return customResponse(message="status required",status=400)
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return customResponse(message= 'Order not found', status=status.HTTP_404_NOT_FOUND)

        if status==1:
            order.statusName = "Accepted by delivery partner"
            order.deliveryPartner_id=request.user.id
        if status==2:
            order.statusName="Picked up"
        if(status==3):
            order.statusName=="Delivered"
        order.status=status
        order.save()
        return customResponse(message="Orders accepted successfully",status=200)




class CreateProduct(APIView):
    def post(self,request,pk=None):
        serializer=ProductSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return customResponse(message='Product Created sucessfully', status=200, data=serializer.data)
        return customResponse(message='Failed to create product', status=400, data=serializer.errors)
    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class OnboardDeliveryPartner(APIView):
    def post(self,request,pk=None):
        mutable_data = request.data.copy() 
        mutable_data['id'] = request.user.id
        try:
            partner = DeliveryPartner.objects.get(id=mutable_data['id'])  # Fetch the partner if exists
            serializer = DeliveryPartnerSerializer(partner, data=mutable_data, partial=True)
        except DeliveryPartner.DoesNotExist:
            # If no partner exists with the given id, treat it as a new object creation
            serializer = DeliveryPartnerSerializer(data=mutable_data, partial=True)

        if(serializer.is_valid()):
            serializer.save()
            return customResponse(message='Data updated sucessfully', status=200, data=serializer.data)
        return customResponse(message='Failed to update data', status=400, data=serializer.errors)
        