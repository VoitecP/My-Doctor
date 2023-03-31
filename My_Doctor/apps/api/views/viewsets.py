from apps.core.models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication


class LoginUserViewSet(GenericViewSet):

    permission_classes = [AllowAny]
    serializer_class=LoginUserSerializer

    @action(detail=False, methods=["post"], url_path='login')   # , serializer_class=LoginUserSerializer) 
    def user_login(self, request):                              # , *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user  is not None :
                login(request, user)
                return Response({"Successfully logged in": request.user.username}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)

    


class PatientViewSet(ModelViewSet):
    queryset=Patient.objects.all()
    serializer_class=PatientSerializer
    # permission_classes=[IsAuthenticated, SessionAuthentication]
    permission_classes=[IsAuthenticated]
    
    # filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class=PatientFilter        
    # search_fields=['name','surname','citizen_id']
    # ordering_fields=['citizen_id', 'name', 'surname'] 


