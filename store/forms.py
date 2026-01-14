from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 4, "class": "form-control", "maxlength": 1000}),
        }

    def clean_comment(self):
        comment = (self.cleaned_data.get("comment") or "").strip()
        if len(comment) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters.")
        return comment
