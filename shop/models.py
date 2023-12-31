from django.db import models


class Currency(models.Model):

    name = models.CharField(max_length=3, verbose_name='Currency')

    def __str__(self):
        return self.name


class Item(models.Model):

    name = models.CharField(max_length=150, verbose_name='Product name')
    description = models.TextField(verbose_name='Product description')
    price = models.FloatField(verbose_name='Product price')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Order(models.Model):

    name = models.CharField(max_length=250)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.FloatField(verbose_name='Total price', null=True, blank=True)


class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    """
    Промежуточная модель между Order и Item
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Item price')




