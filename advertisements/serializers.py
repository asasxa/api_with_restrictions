from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):
        """Простановка значения поля создатель."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Валидация: проверяем количество открытых объявлений."""
        user = self.context["request"].user
        if data.get("status") == AdvertisementStatusChoices.OPEN:
            open_ads_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            if open_ads_count >= 10:
                raise serializers.ValidationError("У вас уже есть 10 открытых объявлений.")
        return data
