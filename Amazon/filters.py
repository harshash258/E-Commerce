import django_filters
from .models import Product


class ProductFilters(django_filters.FilterSet):
    CHOICES = (
        ('low-to-high', 'Low-To-High'),
        ('high-to-low', 'High-to-Low')
    )
    sort_by_price = django_filters.ChoiceFilter(label="Sort by Price", choices=CHOICES, method='filter_by_price',)

    class Meta:
        model = Product
        fields = ()

    @staticmethod
    def filter_by_price(queryset, name, value):
        expression = 'productDiscountedPrice' if value == 'low-to-high' else '-productDiscountedPrice'
        return queryset.order_by(expression)
