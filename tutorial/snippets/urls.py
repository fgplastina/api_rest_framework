from django.urls import path,include
from rest_framework.routers import DefaultRouter
from snippets import views
#Como usamos ViewSet en vez de View no es necesario armar las URLs a mano sino que usando routers las automatizamos.

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

