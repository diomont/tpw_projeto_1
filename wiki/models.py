from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def upload_path(instance, filename):
    return settings.UPLOAD_PATH + 'filename'


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=80)
    popularity = models.IntegerField()

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=800)
    main_text = models.TextField()
    main_image = models.ImageField(upload_to=upload_path)

    # JSON format should be verified in views.py code
    side_card = models.JSONField()
    categories = models.ManyToManyField(Category)

    date_created = models.DateTimeField()
    date_last_modified = models.DateTimeField()
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="creator"
    )
    last_modified_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

    edit_restriction_level = models.IntegerField()

    def __str__(self):
        return self.title


class Section(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=120)
    text = models.TextField()
    image = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return self.title
