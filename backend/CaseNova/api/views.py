from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response, status, APIView
from rest_framework.decorators import action
from django.db.models import Prefetch
from .serializers import (
    CaseReadSerializer, CaseWriteSerializer, SkinReadSerializer,
    OpenCaseSerializer, SkinTransactionSerializer, SkinWriteSerializer,
    UserSerializer, UpgradeSerializer)
from cases.models import Case, Skin, SkinTransaction, CaseSkin
from authentication.models import User
from .services import CaseService, TransactionService
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from .paginators import InventoryPagination

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=('GET',), detail=True)
    def inventory(self, request, pk):
        user = User.objects.get(pk=pk)
        inventory = SkinTransaction.objects.filter(user=user)
        paginator = InventoryPagination()
        page = paginator.paginate_queryset(inventory, request, view=self)
        if page is not None:
            serializer = SkinTransactionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = SkinTransactionSerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SkinViewSet(ModelViewSet):
    queryset = Skin.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SkinReadSerializer
        return SkinWriteSerializer


class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all()
    permission_class = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CaseReadSerializer
        return CaseWriteSerializer

    @action(detail=True, methods=('GET',))
    def open_case(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        case = get_object_or_404(
            Case.objects.prefetch_related('skins'),
            pk=pk
        )
        skin = CaseService.open_case(case=case, user=request.user)
        print(type(skin))
        serialized_skin = SkinReadSerializer(skin)
        return Response(data=serialized_skin.data,
                        status=status.HTTP_200_OK)


class SkinTransactionViewSet(ModelViewSet):
    queryset = SkinTransaction.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SkinTransactionSerializer

    @action(methods=('PUT',), detail=True)
    def sell_item(self, request, pk):
        user = request.user
        transaction = get_object_or_404(SkinTransaction, pk=pk)
        modified_transaction = TransactionService.sell_item(user, transaction)
        serializer = self.get_serializer_class()(modified_transaction)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('GET',))
    def latest(self, request):
        count = int(request.query_params.get('count', 20))
        transactions = SkinTransaction.objects.all()[:count]
        serializer = self.get_serializer_class()(transactions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    



@api_view(('POST',))
def upgrade(request):
    serializer = UpgradeSerializer(data=request.data, context={'request', request})
    serializer.is_valid()
    pass # TODO