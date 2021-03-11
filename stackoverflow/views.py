from django.shortcuts import render
from rest_framework.views import APIView
from .utils import StackOverFlow
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .throttle import AnonDayThrottle, AnonMinThrottle

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SearchView(APIView):
    throttle_classes = [AnonMinThrottle, AnonDayThrottle]

    def get(self, request):
        stackover = StackOverFlow()
        query_params = self.request.query_params
        if len(query_params) > 0:
            valid = stackover.check_query_params(query_params)
            if not valid:
                return Response({"message": "Query params not valid"}, status=status.HTTP_400_BAD_REQUEST)

        url = stackover.build_payload(query_params)
        try:
            if url in cache:
                res = cache.get(url)
            else:
                res = requests.get(url)
                cache.set(url, res, timeout=CACHE_TTL)

            if res.status_code == 200:
                import pdb
                # pdb.set_trace()
                return Response({"success": res.json()}, status=status.HTTP_200_OK)
            else:
                raise Exception(str(status.HTTP_400_BAD_REQUEST))
        except Exception as err:
            return Response({"error": 'Error Happended'}, status=status.HTTP_400_BAD_REQUEST)


