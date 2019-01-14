# Generated by Django 2.1.4 on 2019-01-05 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("zengo", "0005_auto_20190102_0308")]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="zengo.Ticket",
            ),
        )
    ]