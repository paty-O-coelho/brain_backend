# producers/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_cpf_cnpj(value):
    digits = re.sub(r"\D", "", value)
    if len(digits) not in [11, 14]:
        raise ValidationError(_("CPF/CNPJ inválido."))


class Producer(models.Model):
    name = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(
        max_length=18, unique=True, validators=[validate_cpf_cnpj]
    )

    def __str__(self):
        return f"{self.name} - {self.cpf_cnpj}"


class Farm(models.Model):
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name="farms"
    )
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    total_area = models.FloatField()
    farming_area = models.FloatField()
    vegetation_area = models.FloatField()

    def clean(self):
        if self.farming_area + self.vegetation_area > self.total_area:
            raise ValidationError(
                _(
                    "A soma das áreas agricultável e de vegetação não pode exceder a área total."
                )
            )

    def __str__(self):
        return self.name


class Harvest(models.Model):
    year = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.year


class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="crops")
    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE, related_name="crops")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("farm", "harvest", "name")

    def __str__(self):
        return f"{self.name} ({self.harvest})"
