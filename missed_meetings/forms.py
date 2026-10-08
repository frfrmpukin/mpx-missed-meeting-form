from django import forms

from .models import MissedMeetingReport


class MissedMeetingReportForm(forms.ModelForm):
    class Meta:
        model = MissedMeetingReport
        fields = ("meeting_date", "comments")
        widgets = {
            "meeting_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "comments": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),
        }
        help_texts = {
            "comments": "Optional. Up to 500 characters.",
        }
