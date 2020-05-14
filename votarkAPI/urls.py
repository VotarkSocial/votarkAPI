"""babiesAPI URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)
from chat.views import ChatViewSet
from comment.views import CommentViewSet
from follow.views import FollowViewSet
from hashtag.views import HashtagViewSet
from like.views import LikeViewSet
from message.views import MessageViewSet
from post.views import PostViewSet
from report.views import ReportViewSet
from share.views import ShareViewSet
from story.views import StoryViewSet
from topic.views import TopicViewSet
from versus.views import VersusViewSet
from viewedStory.views import ViewedStoryViewSet
from votarkUser.views import VotarkUserViewSet
from vote.views import VoteViewSet

from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()

router.register(r'chat', ChatViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'follow', FollowViewSet)
router.register(r'hashtag', HashtagViewSet)
router.register(r'like', LikeViewSet)
router.register(r'message', MessageViewSet)
router.register(r'post', PostViewSet)
router.register(r'report', ReportViewSet)
router.register(r'share', ShareViewSet)
router.register(r'story', StoryViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'versus', VersusViewSet)
router.register(r'viewed_story', ViewedStoryViewSet)
router.register(r'user', VotarkUserViewSet)
router.register(r'vote', VoteViewSet)

# elapp.com/pets
# elapp.com/api/v1/pets

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)