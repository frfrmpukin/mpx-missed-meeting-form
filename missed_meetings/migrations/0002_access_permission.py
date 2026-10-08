from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("missed_meetings", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="missedmeetingreport",
            options={
                "ordering": ("-meeting_date",),
                "permissions": [
                    (
                        "access_missed_meeting_reports",
                        "Can access missed meeting reports",
                    ),
                    ("view_all_reports", "Can view all missed meeting reports"),
                ],
                "verbose_name": "missed meeting report",
                "verbose_name_plural": "missed meeting reports",
            },
        ),
    ]
