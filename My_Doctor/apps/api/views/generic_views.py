from rest_framework.generics import ListCreateAPIView
from apps.core.models import Patient, User
from ..serializers import *


class UserFormView(ListCreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserFormSerializer
        # return PhotoListSerializer
        else:
            return UserFormSerializer