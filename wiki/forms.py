from django import forms
from wiki.models import Article, Section


# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "short_description", "main_text", "main_image", "side_card", "categories"]


# TODO: Custom class to transform JSON into form, and correctly save it
# TODO: Show sections of article (from view most likely as a collection of forms)


# https://docs.djangoproject.com/en/3.2/ref/forms/fields/#creating-custom-fields
SectionFormSet = forms.modelformset_factory(Section, fields=("title", "content"), extra=10, max_num=10, setattr("hidden", ))


class SectionWidget(forms.Textarea):
    template_name = "widgets/sidecard.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)

