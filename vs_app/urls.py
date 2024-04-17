from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'machine', views.MachinesViewSet)
router.register(r'production_logs', views.ProductionLogViewSet)

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('api/', include(router.urls)),
    path('main/', views.calculate_oee, name='calculate_oee'),
]