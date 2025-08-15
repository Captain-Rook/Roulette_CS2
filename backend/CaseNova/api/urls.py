from django.urls import path, include
from rest_framework import routers

from api.views import (CaseViewSet, SkinViewSet, UserViewSet, SkinTransactionViewSet)

api_v1_router = routers.DefaultRouter()
api_v1_router.register('cases', CaseViewSet, 'cases')
api_v1_router.register('skins', SkinViewSet, 'skins')
api_v1_router.register('users', UserViewSet, 'users')
api_v1_router.register('transactions', SkinTransactionViewSet, 'transactions')

urlpatterns = [
    # path('v1/inventory/{int:pk}/', inventory),
    path('v1/', include(api_v1_router.urls)),
]
