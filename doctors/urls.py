from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, PatientViewSet,CustomTokenView,SpokenLanguageViewSet
router = DefaultRouter()
router.register("doctors", DoctorViewSet, "doctor")
router.register("patients", PatientViewSet, "patient")
router.register('spoken-language',SpokenLanguageViewSet)



urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", CustomTokenView.as_view(), name="custom-token"),

]
