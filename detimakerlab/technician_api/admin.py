from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import Count
from django.utils.html import format_html

from .models import *

# Register your models here.
from .. import settings

# TODO change the urls for the images shown (Equipments class, image_tag method)
ImageUrl = "http://localhost:8000/img/"


class NumberOfMembersFilter(admin.SimpleListFilter):
    title = 'Number of Students'
    parameter_name = 'number_of_students'

    def lookups(self, request, model_admin):
        return (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6 or more'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.annotate(number=Count('students'))
            if value == "6":
                return queryset.filter(number__gt=int(value) - 1)
            else:
                return queryset.filter(number=value)
        else:
            return queryset


################################################################################
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "mail", "nmec")


class RequestsAdmin(admin.ModelAdmin):

    def request(self, obj):
        return obj

    def project_name(self, obj):
        link = reverse("admin:technician_api_project_change", args=[obj.project_ref.code])
        return format_html('<a href="{}">{}</a>', link, obj.project_ref.short_name)

    def equipment_link(self, obj):
        link = reverse("admin:technician_api_equipments_change", args=[obj.equipment_ref.ref])
        return format_html('<a href="{}">{}</a>', link, obj.equipment_ref.description)

    ordering = ["id"]
    readonly_fields = ('timestamp', 'dateAcknowledged')
    list_display = ("request", "project_name", "equipment_link", "status", "timestamp", "dateAcknowledged")
    search_fields = (
        'id', 'equipment_ref__description', 'equipment_ref__family', 'project_ref__short_name', 'project_ref__name')

    list_filter = ['status']
    request.admin_order_field = 'id'
    request.short_description = 'Request id'

    project_name.admin_order_field = 'project_ref__short_name'
    project_name.short_description = 'Project requesting'

    equipment_link.short_description = 'Requested Equipment'
    equipment_link.admin_order_field = 'equipment_ref__description'


class GroupAdmin(admin.ModelAdmin):
    class StudentsInline(admin.TabularInline):
        model = Group.students.through
        extra = 0

    # Student list with html links
    def students_list(self, obj):
        multiline = True
        studentList = [p for p in obj.students.all()]
        links = [(reverse("admin:technician_api_student_change", args=[student.nmec])) for student in studentList]

        urls = []
        for student, link in zip(studentList, links):
            if multiline:
                urls.append(format_html('<p> <a href="{}">{}</a> </p>', link, student.name))
            else:
                urls.append(format_html('<a href="{}">{}</a>', link, student.name))

        html = ''
        for url in urls:
            html += url

        return format_html(html)

    def number_of_members(self, obj):
        return obj.students.count()

    def project_link(self, obj):
        link = reverse("admin:technician_api_project_change", args=[obj.cod_project.code])
        return format_html('<a href="{}">{}</a>', link, obj.cod_project.short_name)

    list_display = ["cod_group", "group_number", "project_link", "students_list"]
    search_fields = ["cod_group", "group_number", "students__name", "cod_project__short_name"]
    list_filter = (NumberOfMembersFilter,)

    inlines = [
        StudentsInline,
    ]

    filter_horizontal = ('students',)

    project_link.short_description = 'project'
    project_link.admin_order_field = 'cod_project__short_name'


class EquipmentAdmin(admin.ModelAdmin):

    # Image Processing
    def image_tag(self, obj):
        return format_html(
            '<p> <a href="{0}"> <img src="{0}" width="20" height="20" /> </a> </p>'.format(
                ImageUrl + str(obj.image_file)))

    def make_unavailable(self, request, queryset):
        queryset.update(status='ind')

    def make_available(self, request, queryset):
        queryset.update(status='dis')

    ordering = ["ref"]
    list_display = ["ref", "family", "description", "location", "price", "broken", "status", "borrowed_items",
                    "total_items", "image_tag"]
    list_filter = ("family", "broken", "status")
    search_fields = ["ref", "family", "description", "location", "price", "broken", "status", "borrowed_items",
                     "total_items", ]

    actions = ["make_unavailable", "make_available"]

    make_available.short_description = "Mark selected Equipments as available"
    make_unavailable.short_description = "Mark selected Equipments as unavailable"
    image_tag.short_description = 'Image'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["code", "short_name", "name", "year", "semester"]
    search_fields = ["code", "short_name", "name", "year", "semester"]
    list_filter = ["year", "semester"]


class EntrancesAdmin(admin.ModelAdmin):
    def entrance(self, obj):
        return obj

    def equipment_link(self, obj):
        link = reverse("admin:technician_api_equipments_change", args=[obj.component_ref.ref])
        return format_html('<a href="{}">{}</a>', link, obj.component_ref.description)

    list_display = ['entrance', 'equipment_link', 'quantity', 'date', 'supplier', 'price_iva', 'price_unity']
    search_fields = ['id', 'component_ref__description', 'quantity', 'date', 'supplier', 'price_iva', 'price_unity']

    entrance.admin_order_field = 'id'
    entrance.short_description = 'Entrance id'


class ExitAdmin(admin.ModelAdmin):

    def exit(self, obj):
        return obj

    def equipment_link(self, obj):
        link = reverse("admin:technician_api_equipments_change", args=[obj.component_ref.ref])
        return format_html('<a href="{}">{}</a>', link, obj.component_ref.description)

    def project_link(self, obj):
        link = reverse("admin:technician_api_project_change", args=[obj.project.code])
        return format_html('<a href="{}">{}</a>', link, obj.project.short_name)

    def group_link(self, obj):
        link = reverse("admin:technician_api_group_change", args=[obj.group.cod_group])
        return format_html('<a href="{}">{}</a>', link, obj.group.group_number)

    readonly_fields = ('timestamp',)
    list_display = ['exit', 'equipment_link', 'quantity', 'year', 'project_link', 'group_link', 'timestamp']
    search_fields = ['id', 'component_ref__description', 'quantity', 'year', 'project__name', 'project__short_name',
                     'group__group_number', 'timestamp']

    exit.admin_order_field = 'id'
    exit.short_description = 'Exit id'

    equipment_link.admin_order_field = 'component_ref__ref'
    project_link.admin_order_field = 'project__short_name'
    group_link.admin_order_field = 'group__number'


admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Request, RequestsAdmin)
admin.site.register(Exit, ExitAdmin)
admin.site.register(Equipments, EquipmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Entrance, EntrancesAdmin)
admin.site.register(Missing)
