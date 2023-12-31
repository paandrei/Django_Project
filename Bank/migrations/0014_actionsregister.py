# Generated by Django 4.2.6 on 2023-11-01 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Bank", "0013_feedback"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActionsRegister",
            fields=[
                (
                    "iban",
                    models.CharField(max_length=14, primary_key=True, serialize=False),
                ),
                ("action_name", models.CharField(default="", max_length=50)),
                ("date", models.DateField(default=None)),
                ("amount", models.FloatField(default=0.0)),
                (
                    "username",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Bank.account",
                    ),
                ),
            ],
            options={
                "db_table": "Register",
            },
        ),
    ]
