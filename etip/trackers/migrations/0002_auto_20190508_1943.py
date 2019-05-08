# Generated by Django 2.0.13 on 2019-05-08 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackers', '0001_squashed_0008_auto_20180401_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackerCategory',
            fields=[
                ('category_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trackers.Category')),
            ],
            bases=('trackers.category',),
        ),
        migrations.RenameField(
            model_name='tracker',
            old_name='short_description',
            new_name='comments',
        ),
        migrations.AddField(
            model_name='tracker',
            name='category',
            field=models.ManyToManyField(blank=True, to='trackers.TrackerCategory'),
        ),
    ]
