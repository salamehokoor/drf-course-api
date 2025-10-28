from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics


class ProductListAPIView(generics.ListAPIView):
    """
    View to list all products in the inventory.
    """
    queryset = Product.objects.filter(stock__gt=0)
    #stock → is the model field (e.g., the number of items available).
    #__gt → means “greater than”.
    #Together, stock__gt=0 means:
    #“Get all Product objects where the stock value is greater than 0.”
    serializer_class = ProductSerializer


#@api_view(['GET'])
#Only GET requests are allowed.
#"This is an API View."
#def product_list(request):
#   """
#   View to list all products in the inventory.
#    """
#    products = Product.objects.all()
#    serializer = ProductSerializer(products, many=True)
#    return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    View to retrieve a specific product by its primary key (pk).
    """
    #There is a bit of magic happening here: we have a PK in the URL pattern (products/<int:pk>/).
    #but we dont have any reference to pk in this view.
    #Django REST Framework automatically picks up the pk from the URL and uses it to retrieve the correct Product instance.
    #lookup_field = 'pk'  # This is the default, so it's optional to specify it.
    #lookup_url_kwarg = 'pk'  # This is also the default.
    #we can change the name of the value we are getting from the url and then change the lookup_url_kwarg to match it.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#@api_view(['GET'])
#def product_detail(request, pk):
#    """
#    View to list all products in the inventory.
#    """
#    product = get_object_or_404(Product, pk=pk)
#    serializer = ProductSerializer(product)
#    return Response(serializer.data)


class OrderListAPIView(generics.ListAPIView):
    """
    View to list all products in the inventory.
    """
    queryset = Order.objects.prefetch_related('items__product')
    #stock → is the model field (e.g., the number of items available).
    #__gt → means “greater than”.
    #Together, stock__gt=0 means:
    #“Get all Product objects where the stock value is greater than 0.”
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    """
    View to list all products in the inventory .
    """
    queryset = Order.objects.prefetch_related('items__product')
    #It defines the base set of objects the view will work with.
    #Here, it fetches all Order objects and optimizes queries
    #When we get orders, also fetch all their related items
    #And for each item, fetch the related product
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        #Calls the parent class (ListAPIView) to get the base queryset defined earlier.
        #So now qs = all orders (with their prefetched items and products).
        return qs.filter(user=self.request.user)
        #Filters that queryset to include only the orders that belong to the current logged-in user.
        #self.request.user gives the user who made the API request.
        #but a problem arises if the user is not authenticated.
        #so now we need to tell django that this view is only accessible to authenticated users.


#@api_view(['GET'])
#Only GET requests are allowed.
#"This is an API View."
#def order_list(request):
#    """
#    View to list all Orders in the inventory.
#    """
#    orders = Order.objects.prefetch_related('items__product')
#    #prefetch_related() tells Django:
#“Go fetch all the related objects I’ll need in advance — in as few queries as possible.”
#Django runs multiple queries, then joins them in Python memory, so you avoid repeated hits to the database.
#This uses Django’s double underscore syntax (__) to go one level deeper in relationships.
#'items__product' means:
#“When fetching Orders, prefetch the related OrderItems (items),
#and for each of those OrderItems, also prefetch their related Products.”
#    serializer = OrderSerializer(orders, many=True)
#    return Response(serializer.data)


@api_view(['GET'])
def product_info(request):

    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':
        products,
        'count':
        len(products),
        'max_price':
        products.aggregate(max_price=Max('price'))['max_price'],
    })
    return Response(serializer.data)
