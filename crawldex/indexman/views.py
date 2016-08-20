import hashlib
import redis
from django.http.response import HttpResponse
from indexman.models import MappingUrlTimestamp
from indexman.serializers import MappingUrlTimestampSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class RawHTMLSearchView(APIView):

    def get(self, request, format=None):
        qp = request.query_params
        url = qp['url']
        assert url, "The url is not sent."
        version = int(qp['version'])
        assert version, "The version is not sent"
        as_html = bool(qp.get('as_html', False))

        md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        objects = MappingUrlTimestamp.objects.filter(md5=md5).order_by(
            '-indexed_timestamp')
        try:
            v_object = objects[version]
        except (TypeError, KeyError):
            return Response('Not Found', status=404)

        r = redis.StrictRedis()
        raw = r.get('{}__{}'.format(v_object.md5, v_object.indexed_timestamp))
        if not raw:
            raise Exception('Redis empty')

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
