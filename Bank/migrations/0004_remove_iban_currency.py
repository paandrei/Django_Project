# Generated by Django 4.2.6 on 2023-10-19 12:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Bank", "0003_remove_account_iban_alter_account_id_iban"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="iban",
            name="currency",
        ),
    ]
