from django.db import models
from django.core.validators import RegexValidator


class categories(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=20)
    friendly_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

    def use_friendly_name(self):
        return self.friendly_name


class products(models.Model):
    # meta class to edit how it looks in django admin panel
    class Meta:
        verbose_name_plural = 'Products'

    # error message when a wrong format entered
    date_message = 'Please enter YYYY format'

    # desired format
    date_regex = RegexValidator(
        regex=r'[1-2][0-9][0-9][0-9]',
        message=date_message
    )

    name = models.CharField(max_length=50)
    category = models.ForeignKey('categories', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    image = models.ImageField()
    date = models.CharField(validators=[date_regex], max_length=60,
                            null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class sizes(models.Model):
    class Meta:
        verbose_name_plural = 'Sizes'

    # both required fields as needed for pricing
    sizes = models.CharField(max_length=10)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.sizes


class finish(models.Model):
    class Meta:
        verbose_name_plural = 'Finishes'

    # both required fields as needed for pricing
    finish = models.CharField(max_length=50)
    # 2 decimal places, like currency is written
    price = models.DecimalField(max_digits=6, decimal_places=2)
    friendly_name = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.finish

    def use_friendly_name(self):
        return self.friendly_name
