from indexman.models import MappingUrlTimestamp
from rest_framework.serializers import ModelSerializer


class MappingUrlTimestampSerializer(ModelSerializer):

    class Meta:
        model = MappingUrlTimestamp
