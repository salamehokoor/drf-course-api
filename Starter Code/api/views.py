from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max


@api_view(['GET'])
#Only GET requests are allowed.
#"This is an API View."
def product_list(request):
    """
    View to list all products in the inventory.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    """
    View to list all products in the inventory.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
#Only GET requests are allowed.
#"This is an API View."
def order_list(request):
    """
    View to list all Orders in the inventory.
    """
    orders = Order.objects.prefetch_related('items__product')
    #prefetch_related() tells Django:
    #“Go fetch all the related objects I’ll need in advance — in as few queries as possible.”
    #Django runs multiple queries, then joins them in Python memory, so you avoid repeated hits to the database.
    #This uses Django’s double underscore syntax (__) to go one level deeper in relationships.
    #'items__product' means:
    #“When fetching Orders, prefetch the related OrderItems (items),
    #and for each of those OrderItems, also prefetch their related Products.”
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


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
