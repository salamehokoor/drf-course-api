from django.contrib import admin
from api.models import Order, OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    #What this does:
    #admin.TabularInline means that you want to display related items in a table-style inline form inside another model’s admin page.
    #model = OrderItem → tells Django that this inline form is for the OrderItem model.


class OrderAdmin(admin.ModelAdmin):
    """""
    What this does:
        This tells Django that when you open an Order in the admin,
        it should include the inline OrderItem forms.
    So you can:
        View, add, or edit the Order itself.
        At the same time, manage its related OrderItems directly below it.
    """ ""

    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
#You’re telling Django:
#“Show the Order model in the admin, using the custom admin setup OrderAdmin.”
