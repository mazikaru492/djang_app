from django.db import migrations


def load_employees(apps, schema_editor):
    Employee = apps.get_model('django_book_store', 'Employee')
    rows = [
        ('R20001', '鈴木一郎', 'ry000001'),
        ('R20002', '山田太郎', 'rx000002'),
        ('R20003', '坂本竜馬', 'rw000003'),
        ('R20004', '田中花', 'rv000004'),
    ]
    for employee_no, employee_name, password in rows:
        Employee.objects.using(schema_editor.connection.alias).get_or_create(
            employee_no=employee_no,
            defaults={'employee_name': employee_name, 'password': password},
        )


class Migration(migrations.Migration):
    dependencies = [('django_book_store', '0002_employee')]
    operations = [migrations.RunPython(load_employees, migrations.RunPython.noop)]
