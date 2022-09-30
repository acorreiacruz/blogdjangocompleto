from rest_framework.permissions import BasePermission


class EhDono(BasePermission):

    message = "Um usuário só pode manipular suas próprias receitas"

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)