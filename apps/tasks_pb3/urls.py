from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^logout$', views.logout),
    url(r'^execute_createjob$', views.execute_createjob),
    url(r'^display_viewjob$', views.display_viewjob),
    url(r'^display_viewjob2$', views.display_viewjob2),
    url(r'^display_addjob$', views.display_addjob),
    url(r'^execute_dojob$', views.execute_dojob),
    url(r'^display_editjob$', views.display_editjob),
    url(r'^execute_updatejob$', views.execute_updatejob),
    url(r'^execute_canceljob$', views.execute_canceljob),

    url(r'^execute_jobdone$', views.execute_jobdone),



    

]