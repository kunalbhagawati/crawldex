from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RawHTMLSearchView(APIView):

    def get(self, request, format=None):
        return Response("Hi")


class URLSearchView(APIView):

    def get(self, request, format=None):
        return Response("Hi")
