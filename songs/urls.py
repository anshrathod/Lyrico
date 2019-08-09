from django.urls import path

from users import views as uviews

from . import views as sviews

urlpatterns = [
    
    path('',sviews.home,name='songs-home'),
    path('songs/list',sviews.list,name='songs-listsongs'),
    path('songs/details/<int:pk>/',sviews.SongDetailView.as_view(), name='songs-details'),
    path('about/',sviews.about, name='songs-about'),
    path('accounts/login/',uviews.login_user , name='songs-login'),
    path('add/',uviews.addsong, name='songs-add'),
    path('signup/',uviews.register , name='songs-signup'),
    path('profile/',uviews.profile,name='songs-profile'),
    path('profile/add/',uviews.addprofile,name='songs-addprofile'),
    path('profile/update/',uviews.update,name='songs-update'),
    path('logout/',uviews.logout_user , name='songs-logout'),
    path('password/change/',uviews.changepass,name='songs-password'),
    path('songs/delete/<int:pk>/',sviews.SongDeleteView.as_view(),name='songs-delete'),
    path('songs/update/<int:pk>/',sviews.updatesong,name='songs-updatesong')
]