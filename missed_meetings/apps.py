from django.apps import AppConfig


class MissedMeetingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "missed_meetings"
    label = "missed_meetings"
    verbose_name = "Missed Meeting Reports"
