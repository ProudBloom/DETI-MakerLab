# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import sys

from django.db import models
from django.urls import reverse


class Equipments(models.Model):
    family = models.CharField(max_length=100, help_text="Enter the family of the component")
    ref = models.CharField(primary_key=True, max_length=32)
    description = models.CharField(max_length=100, help_text="Enter the description of the product")
    location = models.CharField(max_length=10, help_text="Location of equipment")
    total_items = models.IntegerField()
    borrowed_items = models.IntegerField()
    price = models.FloatField()
    BROKEN = (
        ('yes', 'broken'),
        ('no', 'ok'),
    )
    broken = models.CharField(max_length=3, choices=BROKEN, blank=True, default='no',
                              help_text='Condition of the equipment')
    STATUS = (
        ('dis', 'Available'),
        ('ind', 'Unavailable'),
    )
    status = models.CharField(max_length=3, choices=STATUS, blank=True, default='dis', help_text='Status of equipment')
    image_file = models.ImageField(upload_to='equipment', blank=True)   # uploads the image to the equipments folder (/media/equipmets/file.jpg)

    def borrow_equipment(self):
        if self.borrowed_items >= self.total_items:
            print('Error. Borrow > total')
            sys.exit(1)
        self.borrowed_items += 1
        self.save()

    def return_equipment(self):
        if self.borrowed_items == 0:
            sys.exit(1)
        self.borrowed_items -= 1
        self.save()

    def set_status(self):
        if self.total_items <= self.borrowed_items:
            self.status = 'ind'
            self.save()
        elif self.broken == 'yes':
            self.status = 'rep'
            self.save()
        else:
            self.status = 'dis'
            self.save()

    def add_equipment(self):
        """
            change the qtdy of equipemnt in the lab
        :return:
        """
        self.total_items += 1

    def change_qtdy_equipment(self, new_qtdy):
        """
            change the qtdy of equipemnt in the lab
        :return:
        """
        self.total_items = new_qtdy

    def check_availability(self):
        if self.borrowed_items == self.total_items:
            return False
        return True

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Equipments.
        """
        return reverse('equipment-detail-view', args=[str(self.ref)])

    def __str__(self):
        return self.description


class Project(models.Model):
    code = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    year = models.IntegerField()
    semester = models.IntegerField()
    equipment = models.ManyToManyField(Equipments)

    def __str__(self):
        return self.short_name


class Student(models.Model):  # Student also works as teacher (so is more like a USER table than a student table)
    nmec = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    mail = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Group(models.Model):
    cod_group = models.CharField(max_length=32, primary_key=True)
    year = models.IntegerField()
    group_number = models.IntegerField()
    cod_project = models.ForeignKey(  # One group can have one projects
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    teacher = models.CharField(max_length=64, blank=True)
    students = models.ManyToManyField(Student, blank=False)

    def __str__(self):
        return self.cod_group


class Entrance(models.Model):  # table from when a new item is added
    id = models.AutoField(primary_key=True)
    component_ref = models.OneToOneField(Equipments, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    supplier = models.CharField(max_length=64)
    price_iva = models.IntegerField()
    price_unity = models.CharField(max_length=16)


class Exit(models.Model):  # when an item is borrowed
    id = models.AutoField(primary_key=True)
    component_ref = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    year = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the Exit was made


class Request(models.Model):
    id = models.AutoField(primary_key=True)  # Auto generated id
    equipment_ref = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    project_ref = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the request was made
    STATUS = (
        ('pending', 'pending request'),
        ('denied', 'denied'),
        ('approved', 'approved'),
    )
    status = models.CharField(max_length=32, choices=STATUS, blank=False, default='pending',
                              help_text='Status of the request')

    # Functions called to change the status

    def approve(self):
        self.status = "approved"
        self.save()

    def deny(self):
        self.status = "denied"
        self.save()


class Missing(models.Model):
    id = models.AutoField(primary_key=True)  # Auto generated id
    equipment_ref = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    project_ref = models.ForeignKey(Project, on_delete=models.CASCADE)
    group_ref = models.ForeignKey(Group, on_delete=models.CASCADE)
    year = models.CharField(max_length=32)
    reason = models.CharField(max_length=64, null=True)
