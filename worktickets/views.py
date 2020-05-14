from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

from worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType
from worktickets.serializers import (WorkTicketSerializer,
                                     TicketCommentSerializer,
                                     TicketEnclosureSerializer,
                                     TicketTypeSerializer)


class WorkTicketPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('ticket_status', '-create_time', '-update_time')
    serializer_class = WorkTicketSerializer
    pagination_class = WorkTicketPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', 'content', 'type__name')
    ordering_fields = ('level', 'ticket_status', 'create_time', 'update_time')
    filter_fields = ('id', 'ticket_status', 'create_user__username', 'action_user__username')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class TicketCommentViewSet(viewsets.ModelViewSet):
    queryset = TicketComment.objects.all().order_by('create_time')
    serializer_class = TicketCommentSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('ticket__id',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class TicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = TicketEnclosure.objects.all()
    serializer_class = TicketEnclosureSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('ticket__id',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
