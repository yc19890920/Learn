from django_filters import rest_framework as filters
from otest.models import Test

class TestFilter(filters.FilterSet):
    goods_id = filters.CharFilter()
    # goods_id = filters.CharFilter(method='filter_goods_id')

    class Meta:
        model = Test
        fields = ['goods_id']

    # def filter_search(self, queryset, name, value):
    #     if ',' in value:
    #         return queryset.filter(osku__in=value.split(','))
    #     else:
    #         return queryset.filter(Q(name__icontains=value) |
    #                                Q(osku__icontains=value) |
    #                                Q(sku__icontains=value))

