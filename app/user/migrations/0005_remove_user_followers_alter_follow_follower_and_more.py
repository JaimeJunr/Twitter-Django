# Generated by Django 5.1.1 on 2024-10-02 00:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("user", "0004_alter_user_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="followers",
        ),
        migrations.AlterField(
            model_name="follow",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="Os grupos aos quais este usuário pertence.",
                related_name="custom_user_set",
                to="auth.group",
                verbose_name="Grupos",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Permissões específicas para este usuário.",
                related_name="custom_user_permissions_set",
                to="auth.permission",
                verbose_name="Permissões do usuário",
            ),
        ),
    ]
