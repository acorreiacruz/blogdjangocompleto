from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.models import User
from api.serializers import ReceitasSerializer, UserSerializer
from receitas.models import Receitas
from rest_framework.pagination import PageNumberPagination
from api.permissions import EhDono
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action


class PaginacaoCustomizada(PageNumberPagination):
    page_size = 6


class ReceitaModelViewSet(ModelViewSet):
    queryset = Receitas.objects.all()
    serializer_class = ReceitasSerializer
    pagination_class = PaginacaoCustomizada
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['PATCH', 'DELETE']:
            return [EhDono(),]
        return super().get_permissions(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).order_by('-id')
        categoria = self.request.query_params.get('categoria', '')
        if categoria:
            qs = qs.filter(category=categoria)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            id = self.request.user.id
        )
        return qs

    @action(detail=False, url_path='me', url_name='me')
    def me(self, *args, **kwargs):
        user = self.get_queryset().first()
        serializer = self.get_serializer(instance=user, many=False)
        return Response(data=serializer.data)