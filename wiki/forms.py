from django import forms
from models import Article


# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "short_description", "main_text", "main_image", "side_card", "categories", "sections"]

#class