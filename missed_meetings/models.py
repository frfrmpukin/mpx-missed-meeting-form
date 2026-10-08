from django.conf import settings
from django.db import models


class MissedMeetingReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="missed_meeting_reports",
    )
    meeting_date = models.DateField()
    comments = models.TextField(
        "Questions/Comments/Complaints/Concerns",
        blank=True,
        max_length=500,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-meeting_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "meeting_date"),
                name="unique_missed_meeting_report_per_user_date",
            )
        ]
        permissions = [
            (
                "access_missed_meeting_reports",
                "Can access missed meeting reports",
            ),
            ("view_all_reports", "Can view all missed meeting reports"),
        ]
        verbose_name = "missed meeting report"
        verbose_name_plural = "missed meeting reports"

    def __str__(self):
        return f"{self.user} - {self.meeting_date}"
