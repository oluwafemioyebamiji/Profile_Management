from rest_framework import generics
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from profiles.models import Profile, ProfileStatus
from profiles.serializers import ProfileSerializer, ProfileStatusSerializer, AvatarSerializer
from profiles.permissions import OwnProfileOrReadOnly, OwnerOrReadOnly


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, OwnProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["city"]


class StatusViewSet(ModelViewSet):
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]

    def get_queryset(self):
        queryset = ProfileStatus.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset= queryset.filter(user_profile__user__username = username)
        return queryset
    
    #http://127.0.0.1:8000/api/status/?username=admin

    def perform_create(self, serializers):
        user_profile = self.request.user.profile
        serializers.save(user_profile = user_profile)

class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object