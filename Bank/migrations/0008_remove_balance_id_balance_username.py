# Generated by Django 4.2.6 on 2023-10-19 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Bank", "0007_balance_balance"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="balance",
            name="id",
        ),
        migrations.AddField(
            model_name="balance",
            name="username",
            field=models.CharField(
                default="", max_length=100, primary_key=True, serialize=False
            ),
        ),
    ]
