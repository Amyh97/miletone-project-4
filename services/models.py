from django.db import models


class Services(models.Model):
    class Meta:
        verbose_name_plural = 'Services'

    service = models.CharField(max_length=50)
    image = models.ImageField()
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.service


class Lengths(models.Model):
    class Meta:
        verbose_name_plural = 'Lengths'

    # both required fields as needed for pricing
    length = models.CharField(max_length=10)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.length


class Images(models.Model):
    class Meta:
        verbose_name_plural = 'Images'

    # both required fields as needed for pricing
    images = models.CharField(max_length=50)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.images
