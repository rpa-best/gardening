from uuid import uuid4
from django.db import models


class Camera(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    ip = models.CharField(max_length=255, verbose_name="IP")

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"

    def __str__(self) -> str:
        return self.name
    