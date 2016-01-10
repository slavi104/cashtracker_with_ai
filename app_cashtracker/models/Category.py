from django.db import models
from django.shortcuts import get_object_or_404
from app_cashtracker.models.Subcategory import Subcategory


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey('User')
    is_active = models.BooleanField(default=True)
    DEFAULT_CATEGORIES = {}

    def process(user_id):
        categories = Category.objects.filter(user_id=user_id, is_active=1)
        if categories.count() == 0:
            categories = Category.objects.filter(user_id=1, is_active=1)

        for category in categories:
            Category.DEFAULT_CATEGORIES[category.id] = category.name
            # Category.DEFAULT_CATEGORIES[category.id]['name'] = category.name
            # Category.DEFAULT_CATEGORIES[category.id]['subcategories'] = {}
            # category_subcategories = Subcategory.objects.filter(
            #     category_id=category.id,
            #     is_active=1
            # )
            # for subcategory in category_subcategories:
            #     Category.DEFAULT_CATEGORIES[category.id]['subcategories'][subcategory.id] = subcategory.name

    def get_category_name(category_id=0):
        if not int(category_id):
            return 'All'
        else:
            return get_object_or_404(Category, id=category_id).name

    def __str__(self):
        return self.name
