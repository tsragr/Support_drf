from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('ticket', views.CreateListRetrieveUpdateTicketViewSet, basename='ticket-list_or_create')
router.register('answer', views.CreateAnswerViewSet, basename='answer-create')
router.register('comment', views.CreateCommentViewSet, basename='comment-create')

urlpatterns = router.urls
