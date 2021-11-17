from django.contrib import admin
from wiki.models import Category, Article, Section

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Section)