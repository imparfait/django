# Generated by Django 5.1.4 on 2025-01-24 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_alter_taskgroup_created_by_taskimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='color',
            field=models.CharField(choices=[('#FF5733', 'Red'), ('#33FF57', 'Green'), ('#3357FF', 'Blue'), ('#FFFF33', 'Yellow'), ('#FF33FF', 'Pink'), ('#800080', 'Purple')], default='#000000', max_length=7),
        ),
    ]
