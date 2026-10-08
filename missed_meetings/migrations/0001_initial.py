import django.conf
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(django.conf.settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MissedMeetingReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meeting_date", models.DateField()),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="missed_meeting_reports",
                        to=django.conf.settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "missed meeting report",
                "verbose_name_plural": "missed meeting reports",
                "ordering": ("-meeting_date",),
                "permissions": [
                    ("view_all_reports", "Can view all missed meeting reports")
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="missedmeetingreport",
            constraint=models.UniqueConstraint(
                fields=("user", "meeting_date"),
                name="unique_missed_meeting_report_per_user_date",
            ),
        ),
    ]
