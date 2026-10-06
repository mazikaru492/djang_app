from django.contrib import admin

from .models import Customer, Employee


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'customer_name')
    search_fields = ('customer_code', 'customer_name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_no', 'employee_name')
    search_fields = ('employee_no', 'employee_name')
