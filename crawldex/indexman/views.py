import hashlib
import redis
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from indexman.models import MappingUrlTimestamp
from indexman.serializers import MappingUrlTimestampSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class RawHTMLView(APIView):

    def get(self, request, format=None):
        qp = request.query_params
        url = qp['url']
        assert url, "The url is not sent."
        version = int(qp['version'])
        assert version, "The version is not sent"
        as_html = 'as_html' in qp

        md5 = hashlib.md5(url.encode('utf-8')).hexdigest()

        try:
            obj = MappingUrlTimestamp.objects.get(md5=md5,
                                                  indexed_timestamp=version)
        except ObjectDoesNotExist:
            return Response(status=404)

        r = redis.StrictRedis()
        raw = r.get('{}__{}'.format(obj.md5, obj.indexed_timestamp))
        if not raw:
            raise Exception('Redis empty. Why??')

        return Response(raw) if not as_html else HttpResponse(raw)


class URLSearchView(APIView):

    def get(self, request, format=None):
        qp = request.query_params
        url = qp['url']
        assert url, "The url is not sent."
        md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        objects = MappingUrlTimestamp.objects.filter(md5=md5).order_by(
            '-indexed_timestamp')
        return Response(
            MappingUrlTimestampSerializer(objects, many=True).data)
