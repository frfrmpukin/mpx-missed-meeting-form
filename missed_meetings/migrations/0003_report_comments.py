from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missed_meetings", "0002_access_permission"),
    ]

    operations = [
        migrations.AddField(
            model_name="missedmeetingreport",
            name="comments",
            field=models.TextField(
                blank=True,
                max_length=500,
                verbose_name="Questions/Comments/Complaints/Concerns",
            ),
        ),
    ]
