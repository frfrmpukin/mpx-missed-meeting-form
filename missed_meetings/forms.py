from django import forms

from .models import MissedMeetingReport


class MissedMeetingReportForm(forms.ModelForm):
    class Meta:
        model = MissedMeetingReport
        fields = ("meeting_date",)
        widgets = {
            "meeting_date": forms.DateInput(attrs={"type": "date"}),
        }
