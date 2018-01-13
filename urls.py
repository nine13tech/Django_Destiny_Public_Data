from django.conf.urls import url, include

from . import views

app_name = 'Destiny_Public_Data'
urlpatterns = [
    url(r'^d1/public_quests/$', views.d1_quests, name="d1_quests"),
    url(r'^d2/public_milestones/$', views.d2_public_milestones, name="d2_public_milestones"),
]