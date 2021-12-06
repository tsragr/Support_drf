import django_filters
from tikets import models


class TicketFilter(django_filters.FilterSet):

    class Meta:
        model = models.Ticket
        fields = {
            'status': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }