# from django.apps import AppConfig
from detimakerlab.wiki.apps import WikiConfig


class TechApiConfig(WikiConfig):
    name = 'detimakerlab.technician_api'
    verbose_name = 'DETI MakerLab Technician'
