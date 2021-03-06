# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-15 21:21
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F


def add_to_system_projects(apps, schema_editor):

    Project = apps.get_model('base', 'Project')

    try:
        project = Project.objects.get(slug='pontoon-intro')
    except Project.DoesNotExist:
        return

    project.system_project = True
    project.save()

    # Update Locale stats
    ProjectLocale = apps.get_model('base', 'ProjectLocale')
    for locale in project.locales.all():
        project_locale = ProjectLocale.objects.get(project=project, locale=locale)
        locale.total_strings = F('total_strings') - project_locale.total_strings
        locale.approved_strings = F('approved_strings') - project_locale.approved_strings
        locale.fuzzy_strings = F('fuzzy_strings') - project_locale.fuzzy_strings
        locale.unreviewed_strings = F('unreviewed_strings') - project_locale.unreviewed_strings
        locale.save(update_fields=[
            'total_strings',
            'approved_strings',
            'fuzzy_strings',
            'unreviewed_strings',
        ])


def remove_from_system_projects(apps, schema_editor):

    Project = apps.get_model('base', 'Project')

    try:
        project = Project.objects.get(slug='pontoon-intro')
    except Project.DoesNotExist:
        return

    project.system_project = False
    project.save()

    # Update Locale stats
    ProjectLocale = apps.get_model('base', 'ProjectLocale')
    for locale in project.locales.all():
        project_locale = ProjectLocale.objects.get(project=project, locale=locale)
        locale.total_strings = F('total_strings') + project_locale.total_strings
        locale.approved_strings = F('approved_strings') + project_locale.approved_strings
        locale.fuzzy_strings = F('fuzzy_strings') + project_locale.fuzzy_strings
        locale.unreviewed_strings = F('unreviewed_strings') + project_locale.unreviewed_strings
        locale.save(update_fields=[
            'total_strings',
            'approved_strings',
            'fuzzy_strings',
            'unreviewed_strings',
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0127_project_system_project'),
    ]

    operations = [
        migrations.RunPython(
        	add_to_system_projects,
        	remove_from_system_projects,
        ),
    ]
