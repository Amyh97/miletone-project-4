from django.db import models


class categories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class products(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('categories', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    image = models.ImageField()
    date = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class sizes(models.Model):
    # both required fields as needed for pricing
    sizes = models.CharField(max_length=10)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.sizes


class finish(models.Model):
    # both required fields as needed for pricing
    finish = models.CharField(max_length=10)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.finish
