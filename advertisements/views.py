from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    def check_object_permissions(self, request, obj):
        """Проверка, что пользователь является автором объявления."""
        super().check_object_permissions(request, obj)
        if self.action in ["update", "partial_update", "destroy"]:
            if obj.creator != request.user:
                raise PermissionDenied("Вы не являетесь автором этого объявления.")

    def perform_create(self, serializer):
        """Автоматическая простановка создателя."""
        serializer.save(creator=self.request.user)