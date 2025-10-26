from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Additional fields can be added here as needed.
    """
    pass


class Product(models.Model):
    #models.Model means that Product inherits from Django’s base model class, giving it the ability to interact with the database.
    """
    Model representing a product in the inventory.
    """
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    #TextField is suitable for larger amounts of text compared to CharField.
    #blank=True means that this field is optional in forms (it can be left empty).

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()
    #PositiveIntegerField is an integer that cannot be negative, ensuring that stock counts make sense.

    image = models.ImageField(upload_to='products/', blank=True, null=True)

    #upload_to='products/' specifies the folder in your media directory where the image will be saved.
    #blank=True allows forms to leave this field empty.
    #null=True allows the database to store NULL if no image is provided.

    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

    """
    This is a special method in Python that defines how the object is represented as a string.
    When you print a Product object or see it in the Django admin, it will display the product 
    name instead of something like <Product object at 0x12345>.
    """


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        """
        This is a nested class inside Order used for defining choices for a field.
        models.TextChoices is a Django helper to create enumerated string choices.
        """
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELED = 'Canceled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #By setting it as default, every new order automatically gets a unique UUID without manually assigning it.

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #This creates a relationship to the User model.
    #ForeignKey means each order belongs to one user, but a user can have many orders.
    #on_delete=models.CASCADE means: if the user is deleted, all their orders will also be deleted automatically.

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    products = models.ManyToManyField(
        Product,
        through='OrderItem',
        #Normally, Django creates an automatic join table behind the scenes to handle many-to-many relationships.
        #By using through='OrderItem', you define your own join table.
        related_name='orders',
    )

    #ManyToManyField indicates that an order can contain multiple products, and a product can
    #be part of multiple orders.
    #through='OrderItem' specifies that the relationship is managed through the OrderItem model,
    #which allows for additional fields (like quantity) in the relationship.
    #related_name='orders' allows you to access all orders containing a specific product via product

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    """
    Model representing an item within an order.
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.order_id}"
