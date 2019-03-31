from django.db import models
from main.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Pay(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=300)
    amount_expected = models.DecimalField(decimal_places=8, max_digits=20)
    amount_received = models.DecimalField(decimal_places=8, max_digits=20)
    status = models.CharField(max_length=5, default='0')
    author = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.address


class Order(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    address = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.ForeignKey(Pay, related_name='payment', blank=True, null=True, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



