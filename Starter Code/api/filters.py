import django_filters
from api.models import Product


class InStockFilterBackend(django_filters.rest_framework.DjangoFilterBackend):
    """
    Custom filter backend to filter products that are in stock.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range'],
        }
