from django.urls import path, include
from rest_framework import routers

from .views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet


router = routers.DefaultRouter(trailing_slash=False)


router.register(r'worktickers', WorkTicketViewSet)
router.register(r'ticketcomments', TicketCommentViewSet)
router.register(r'ticketenclosures', TicketEnclosureViewSet)
router.register(r'tickettypes', TicketTypeViewSet)


app_name = 'worktickets'


urlpatterns = [
    path('', include(router.urls)),
]
