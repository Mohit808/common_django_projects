from django.contrib import admin
from .models import OtpModel, Seller, Store, Category ,Brand, Tags , Product, MainCategory, Variant

admin.site.register(OtpModel)
admin.site.register(Seller)
admin.site.register(Store)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Brand)
admin.site.register(Tags)
admin.site.register(Product)


# class CategoryInline(admin.TabularInline):
#     model = Category
#     # extra = 1  # Number of empty forms to display

# class MainCategoryAdmin(admin.ModelAdmin):
#     inlines = [CategoryInline]

# admin.site.register(MainCategory, MainCategoryAdmin)