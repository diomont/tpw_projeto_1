from django import forms
from wiki.models import Article


# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "short_description", "main_text", "main_image", "side_card", "categories"]

#class

# TODO: Custom class to transform JSON into form, and correctly save it
# TODO: Show sections of article (from view most likely as a collection of forms)