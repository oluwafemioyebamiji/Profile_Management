from django.urls import include, path
from profiles.apiviews import ProfileViewSet, StatusViewSet, AvatarUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"profile", ProfileViewSet)
router.register(r"status", StatusViewSet, basename="status")

# profile_list = ProfileViewSet.as_view({"get":"list"})
# profile_detail = ProfileViewSet.as_view({"get":"retrieve"})

urlpatterns = [
    # path('profiles/', profile_list, name= 'profile-list'),
    # path('profiles/<int:pk>/', profile_detail, name= 'profile-detail'),
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar")

] 