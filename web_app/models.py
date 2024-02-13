from django.db import models
from django.contrib.auth import get_user_model


def custom_path(instance, filename):
    return f'media/{filename}'


User = get_user_model()


class Product(models.Model):
    class ProductType(models.IntegerChoices):
        WITH_UNIVERSAL_ITEM = 0
        WITH_UNIQUE_ITEMS = 1

    title = models.CharField(max_length=256,
                             null=False,
                             blank=False,
                             verbose_name="Название")
    description = models.CharField(max_length=1000,
                                   null=False,
                                   blank=False,
                                   verbose_name="Описание")
    product_type = models.IntegerField(choices=ProductType,
                                       verbose_name="Тип товара")
    price = models.DecimalField(max_digits=11,
                                decimal_places=2,
                                verbose_name="Цена")
    photo = models.ImageField(null=False,
                              blank=False,
                              upload_to=custom_path,
                              verbose_name="Картинка")


class Item(models.Model):
    description = models.CharField(max_length=1000,
                                   null=False,
                                   blank=False,
                                   verbose_name="Инструкция")
    file = models.ImageField(null=True,
                             blank=True,
                             upload_to=custom_path,
                             verbose_name="Файл (опционально)")


class Review(models.Model):
    mark = models.IntegerField()
    text = models.CharField(max_length=500, null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


