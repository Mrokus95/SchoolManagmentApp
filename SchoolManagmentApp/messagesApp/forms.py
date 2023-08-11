from django import forms
from .models import Message


class ShortEmailForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget.attrs["class"] = "form-control"


class FullEmailForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["receiver", "title", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receiver"].widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["body"].widget.attrs["class"] = "form-control"
