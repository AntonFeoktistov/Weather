from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=200, verbose_name="Название локации")
    lat = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Широта")
    lon = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Долгота")
    weather_data = models.JSONField(null=True, blank=True)
    weather_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Локация пользователя"
        verbose_name_plural = "Локации пользователей"
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"
