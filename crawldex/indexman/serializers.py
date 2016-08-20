from indexman.models import MappingUrlTimestamp
from rest_framework import serializers


class MappingUrlTimestampSerializer(serializers.ModelSerializer):

    version = serializers.SerializerMethodField()

    def get_version(self, obj):
        return obj.indexed_timestamp

    class Meta:
        model = MappingUrlTimestamp
        fields = ['version']
