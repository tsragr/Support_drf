from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, views
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from . import filters


class CreateListRetrieveUpdateTicketViewSet(viewsets.GenericViewSet,
                                            mixins.CreateModelMixin,
                                            mixins.ListModelMixin,
                                            mixins.UpdateModelMixin,
                                            mixins.RetrieveModelMixin):
    """
    Create -> only authenticated users
    List, Retrieve -> allow any users
    Update status ticket -> only admin user
    """
    queryset = models.Ticket.objects.all()
    serializers = {'create': serializers.CreateTicketSerializer,
                   'list': serializers.ListTicketSerializer,
                   'update': serializers.ChangeStatusSerializer,
                   'partial_update': serializers.ChangeStatusSerializer,
                   'retrieve': serializers.TicketDetailSerializer}

    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.TicketFilter

    def get_serializer_class(self):
        return self.serializers[self.action]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]

        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAdminUser]

        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
        send(self.request.user.email)


    #  @action(detail=True, methods=['put', 'patch'])
    #  def change_status(self, request, pk=None):
    #      instance = get_object_or_404(models.Ticket, pk=pk)
    #      serializer = serializers.ChangeStatusSerializer(instance=instance, data=request.data)
    #      if serializer.is_valid():
    #          serializer.save()
    #      return Response(serializer.data)

class CreateAnswerViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          ):
    """
    Create answer on ticket -> only admin user
    """
    queryset = models.Answer.objects.all()
    serializer_class = serializers.CreateCommentSerializer

    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.validated_data['support'] = self.request.user
        serializer.save()


class CreateCommentViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin):
    """
    Create comment on answer -> only authenticated user
    """
    serializer_class = serializers.CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
