from django.contrib import admin

from .models import *


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "nmec")


admin.site.register(Student, StudentAdmin)


class ExitAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)


admin.site.register(Exit, ExitAdmin)


class RequestsAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)


admin.site.register(Request, RequestsAdmin)

admin.site.register(Group)
admin.site.register(Entrance)
admin.site.register(Equipments)
admin.site.register(Project)
admin.site.register(Missing)
