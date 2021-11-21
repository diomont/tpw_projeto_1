import json

from django import forms
from wiki.models import Article, Section


class ImagePicker(forms.FileInput):
    template_name = "widgets/imagepicker.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def format_value(self, value):
        return value


class SideCardWidget(forms.Widget):
    template_name = "widgets/sidecard.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def format_value(self, value):
        return json.loads(value)


# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "short_description", "main_text", "main_image", "side_card", "categories"]
        widgets = {
            "side_card": SideCardWidget(),
            "main_image": ImagePicker()
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
        self.fields['short_description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Short Description'})
        self.fields['main_text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Main Text'})
        self.fields['categories'].widget.attrs.update({'class': 'form-control w-50'})

# https://docs.djangoproject.com/en/3.2/ref/forms/fields/#creating-custom-fields
SectionFormSet = forms.modelformset_factory(Section, fields=("title", "text", "image"), extra=0,
    widgets={
        "image": ImagePicker(),
        "title": forms.TextInput(attrs={
            "class": "form-control"
        }),
        "text": forms.Textarea(attrs={
            "class": "form-control"
        }),
    })
