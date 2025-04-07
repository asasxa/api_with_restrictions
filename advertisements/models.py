from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"



class Advertisement(models.Model):
    """Объявление."""
    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Валидация: проверяем количество открытых объявлений."""
        if self.status == AdvertisementStatusChoices.OPEN:
            open_ads_count = Advertisement.objects.filter(
                creator=self.creator,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            if open_ads_count >= 10:
                raise ValidationError("У вас уже есть 10 открытых объявлений.")
