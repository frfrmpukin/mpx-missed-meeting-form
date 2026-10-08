from django import forms

from .models import MissedMeetingReport


class MissedMeetingReportForm(forms.ModelForm):
    class Meta:
        model = MissedMeetingReport
        fields = ("meeting_date", "comments")
        widgets = {
            "meeting_date": forms.DateInput(attrs={"type": "date"}),
            "comments": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "comments": "Optional. Up to 500 characters.",
        }
