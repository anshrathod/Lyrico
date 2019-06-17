from django.urls import path
from songs import views as sviews

urlpatterns = [
    
    path('',sviews.home,name='songs-home'),
    path('songs/',sviews.box , name='songs-allsongs',),
    path('songs/list',sviews.list,name='songs-listsongs'),
    path('songs/details/<int:pk>/',sviews.SongDetailView.as_view(), name='songs-songlyrics'),
    path('login/',sviews.login , name='songs-login'),
    path('add/',sviews.addsong, name='songs-add'),
    path('about/',sviews.about, name='songs-about'),

]