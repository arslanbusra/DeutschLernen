from django.db import models


class wordLearning(models.Model):
    nameturkish=models.CharField(max_length=100, verbose_name='Türkçe')
    namedeutsch=models.CharField(max_length=100, verbose_name='Almanca')

    def __str__(self):
        return f"{self.namedeutsch} - {self.nameturkish}"

