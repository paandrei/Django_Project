# Generated by Django 4.2.6 on 2023-10-19 15:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Bank", "0005_balance_remove_account_id_account_iban_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="photo",
        ),
    ]
