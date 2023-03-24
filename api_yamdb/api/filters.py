from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitlesFilter(FilterSet):
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )
    category = CharFilter(
        field_name='category__slug',
    )
    name = CharFilter(
        field_name='name',
    )

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
