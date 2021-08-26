from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions

#Tutorial 5
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

#Tutorial 6 
from rest_framework import viewsets
from rest_framework.decorators import action

@api_view(['GET'])
#format none permite que el server se adapte al formato de la request (si es http responde http, etc, etc)
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# Tutorial 6
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """

    Esta viewset provee automaticamente las acciones 'list' y 'retrieve'

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes =  [permissions.IsAuthenticatedOrReadOnly,
                           IsOwnerOrReadOnly]
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializers):
        serializers.save(owner=self.request.user)
