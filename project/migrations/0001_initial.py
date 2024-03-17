# Generated by Django 5.0.3 on 2024-03-15 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(editable=False, max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('due_date', models.DateTimeField(null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Abandoned', 'Abandoned')], default='Ongoing', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]