from rest_framework import serializers

from detimakerlab.wiki.models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('objects', 'current_revision', 'created', 'modified', 'owner', 'group',
                  'group_read', 'group_write', 'other_read', 'other_write', 'project')