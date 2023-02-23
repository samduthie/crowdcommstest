from datetime import datetime

from django.utils import timezone
from django.db.models import F

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from analytics.models import UserVisit


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        user = request.user if request.user.is_authenticated else None
        user_visit, created = UserVisit.objects.update_or_create(user=user)

        user_visit.visits = F('visits') + 1
        user_visit.save()


        data = {
            'version': 1.0,
            'time': timezone.now(),
            'recent_visitors': '',
            'all_visitors': UserVisit.objects.values('user').distinct().count(),
            'all_visits': UserVisit.objects.count(),
        }



        return Response(data)

