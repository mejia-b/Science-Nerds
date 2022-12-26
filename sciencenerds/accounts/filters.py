import django_filters
from .models import Order, Product
from django_filters import DateFilter, CharFilter


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created",lookup_expr="gte")
    end_date = DateFilter(field_name="date_created",lookup_expr="lte")
    # allows the option to filter by word typed
    product = CharFilter(field_name="product__name", lookup_expr="icontains")
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']