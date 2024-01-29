import uuid

from django.db import models
from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


User = get_user_model()


class Product(models.Model):
    class ProductType(models.IntegerChoices):
        WITH_UNIVERSAL_ITEM = 0
        WITH_UNIQUE_ITEMS = 1

    title = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)
    product_type = models.IntegerField(choices=ProductType)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    file = models.FileField(null=True, upload_to=user_directory_path)


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inner_order = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)


class Review(models.Model):
    mark = models.IntegerField()
    text = models.CharField(max_length=500, null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
