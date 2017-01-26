from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$', views.index, name='app'),
    url(r'^videos/$', views.VideoList.as_view()),
    url(r'^Search$', views.search),
    url(r'^videos/(?P<pk>\d+)/$', views.VideoDetail.as_view(), name='video_detail'),
    url(r'^frames/$', views.FrameList.as_view()),
    url(r'^frames/(?P<pk>\d+)/$', views.FrameDetail.as_view(), name='frames_detail'),
]
