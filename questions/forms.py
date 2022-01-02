from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    answer = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter Your Answer Here",
                "class": "new-class-name two",
                "rows": 20,
                "cols": 120
            }
        )
    )

    class Meta:
        model = Question
        fields = ['answer']
