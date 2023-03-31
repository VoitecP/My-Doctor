from ..views.viewsets import *
from rest_framework.routers import DefaultRouter 
# from rest_framework_nested.routers import NestedDefaultRouter


router=DefaultRouter()
router.register(r'', LoginUserViewSet, basename='viewsets-login')           # Must be pattern  r''  not r'login' or 'login/'
router.register(r'patients', PatientViewSet, basename='viewsets-patients')
# router.register(r'visits', VisitViewSet, basename='viewsets-visits')
# router.register(r'doctors', DoctorViewSet, basename='viewsets-doctors')
# router.register(r'categories', CategoryViewSet, basename='viewsets-categories' )

urlpatterns = router.urls


# nested_router=NestedDefaultRouter
# opinion_router=routers.NestedDefaultRouter(router, "doctors", lookup="opinion_pk" )
# opinion_router.register("opinions",OpinionViewSet, basename="doctor-opinion")


