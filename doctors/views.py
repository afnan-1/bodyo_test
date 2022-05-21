from django.shortcuts import render
from requests import request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from doctors.models import Doctor,Patient, SpokenLanguage
from doctors.serializers import DoctorSerializer, PatientSerializer, SpokenLanguageSerializer
from oauth2_provider.views.base import TokenView
from oauth2_provider.models import get_access_token_model, get_application_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
import json
from oauth2_provider.signals import app_authorized
from django.http import HttpResponse

# Create your views here.
# login view for getting information with logins like (username ...)
class CustomTokenView(TokenView):
    """
    Implements an endpoint to provide access tokens
    The endpoint is used in the following flows:
    * Authorization code
    * Password
    * Client credentials
    """

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
                body["user"] = {
                    "id": token.user.id,
                    "email": token.user.email,
                    "is_admin": token.user.is_superuser,
                    "is_staff": token.user.is_staff,
                }
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response



class DoctorViewSet(ModelViewSet):
    """
    Api for doctors crud operation
    
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.action!="create":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        if self.kwargs["pk"]=="update" or self.kwargs["pk"]=="current" :
            obj = Doctor.objects.filter(pk=self.request.user.id).first()
            return obj
        return super().get_object()




class PatientViewSet(ModelViewSet):
    """
    Api for patients crud operation
    
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        self.queryset = self.queryset.filter(doctor=self.request.user)
        return super().get_queryset()



class SpokenLanguageViewSet(ModelViewSet):

    queryset = SpokenLanguage.objects.all()
    serializer_class = SpokenLanguageSerializer
