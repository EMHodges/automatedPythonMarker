from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    answer = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter Your Answer Here",
                "class": "new-class-name two",
                "rows": 20,
                "cols": 120,
                "onchange": 'validate_then_submit()'
            }
        )
    )

    class Meta:
        model = Submission
        fields = ['answer']
