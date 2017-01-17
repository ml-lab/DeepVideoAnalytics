from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'', view=views.index,name="home")
]
