from django.db import migrations


def create_initial_data(apps, schema_editor):
    RecordStatus = apps.get_model('dds', 'RecordStatus')
    RecordType = apps.get_model('dds', 'RecordType')
    RecordCategory = apps.get_model('dds', 'RecordCategory')
    RecordSubcategory = apps.get_model('dds', 'RecordSubcategory')

    status_names = ['Бизнес', 'Личное', 'Налог']
    type_names = ['Пополнение', 'Списание']

    statuses = {}
    for name in status_names:
        statuses[name], _ = RecordStatus.objects.get_or_create(name=name)

    types = {}
    for name in type_names:
        types[name], _ = RecordType.objects.get_or_create(name=name)

    infra_category, _ = RecordCategory.objects.get_or_create(
        name='Инфраструктура',
        type=types['Пополнение'],
    )
    marketing_category, _ = RecordCategory.objects.get_or_create(
        name='Маркетинг',
        type=types['Списание'],
    )

    RecordSubcategory.objects.get_or_create(name='VPS', category=infra_category)
    RecordSubcategory.objects.get_or_create(name='Proxy', category=infra_category)
    RecordSubcategory.objects.get_or_create(name='Farpost', category=marketing_category)
    RecordSubcategory.objects.get_or_create(name='Avito', category=marketing_category)


class Migration(migrations.Migration):

    dependencies = [
        ('dds', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
