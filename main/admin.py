from django.contrib import admin
from .models import Product, ProductImage, Category,Favorite
from django.contrib import admin
from .models import ContactMessage, Order, OrderItem
from django.contrib import admin
from .models import UserProfile



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price')
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Favorite)




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    inlines = [OrderItemInline]




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_moderator', 'is_blocked')

admin.site.register(UserProfile, UserProfileAdmin)