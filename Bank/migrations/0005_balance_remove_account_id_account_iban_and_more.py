# Generated by Django 4.2.6 on 2023-10-19 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Bank", "0004_remove_iban_currency"),
    ]

    operations = [
        migrations.CreateModel(
            name="Balance",
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
            ],
            options={
                "db_table": "Balance",
            },
        ),
        migrations.RemoveField(
            model_name="account",
            name="id",
        ),
        migrations.AddField(
            model_name="account",
            name="iban",
            field=models.CharField(default=None, max_length=14),
        ),
        migrations.AlterField(
            model_name="account",
            name="username",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name="Iban",
        ),
        migrations.AddField(
            model_name="balance",
            name="iban",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Bank.account",
            ),
        ),
    ]
