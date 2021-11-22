import json

from django import forms
from wiki.models import Article, Section


class ImagePicker(forms.FileInput):
    template_name = "widgets/imagepicker.html"

    def format_value(self, value):
        return value


class SideCardWidget(forms.Widget):
    template_name = "widgets/sidecard.html"

    def format_value(self, value):
        return json.loads(value)

    def value_from_datadict(self, data, files, name):
        dics = []
        for key, val in [(key, val) for key, val in data.items() if "_scard_entry_name" in key]:
            dic = {}

            truekey = data.get(key)
            val = data.get(key[:-4] + "val")

            values = val.split("\r\n")
            dic["name"] = truekey
            dic["value"] = values
            dics.append(dic)
        return dics


# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["id", "title", "short_description", "main_text", "main_image", "side_card",
                  "categories", "edit_restriction_level"]
        widgets = {
            "id": forms.HiddenInput(),
            "side_card": SideCardWidget(),
            "main_image": ImagePicker()
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
        self.fields['short_description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Short Description'})
        self.fields['main_text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Main Text'})
        self.fields['categories'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['edit_restriction_level'].widget.attrs.update({'max': 2, 'min': 0, 'value': 0 , 'class': 'form-control'})


# https://docs.djangoproject.com/en/3.2/ref/forms/fields/#creating-custom-fields
SectionFormSet = forms.modelformset_factory(Section, fields=("id", "title", "text", "image"), extra=0,
    widgets={
        "id": forms.HiddenInput(),
        "image": ImagePicker(),
        "title": forms.TextInput(attrs={
            "class": "form-control"
        }),
        "text": forms.Textarea(attrs={
            "class": "form-control"
        }),
    })
