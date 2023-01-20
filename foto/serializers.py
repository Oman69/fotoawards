from rest_framework import routers, serializers, viewsets, permissions
from django.contrib.auth.models import User


from foto.models import Foto, Comments


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    "Список пользователей"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class FotoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Foto
        fields = '__all__'

    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

class FotoViewSet(viewsets.ModelViewSet):
    "Список фото"
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    permission_classes = [permissions.IsAuthenticated]



class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

class CommentsViewSet(viewsets.ModelViewSet):
    "Список фото"
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('fotos', FotoViewSet)
router.register('comments', CommentsViewSet)