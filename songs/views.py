from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)

from songs.models import Song
from users.models import Profile
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
	if request.method =='POST':
		songs = Song.objects.all()
		searchterm=''
		if 'search' in request.POST:
			searchterm = request.POST['search']
			songs1=songs.filter(title__contains=searchterm)
			songs2=songs.filter(composer__contains=searchterm)
			songs3=songs.filter(featuring__contains=searchterm)
			songs=songs1|songs2|songs3
		songz = zip(songs,range(len(songs)+1)[1:])
		context = {'searchterm': searchterm,'songs':songz}
		return render(request, 'songs/listview.html', context) 
	return render(request,'songs/base.html')

def updatesong(request,pk):
	song = Song.objects.get(id=pk)
	if request.user.username == song.composer:
		if request.method == 'POST':
			title = request.POST['title']
			lyrics = request.POST['lyrics']
			try:
				if request.FILES['image']:
					image = request.FILES['image']
					path = song.img.path
					import os
					os.remove(path)
					song.img = image 
				else:
					image = song.img
					song.img = image
			except MultiValueDictKeyError :
				image = song.img
				song.img = image
			try:
				if request.FILES['audio']!= song.audio:
					audio = request.FILES['audio']
					path = song.audio.path
					import os
					os.remove(path)
					song.audio = audio
				else:
					audio = song.audio
					song.audio = audio
			except MultiValueDictKeyError:
				audio = song.audio
				song.audio = audio
			ytlink = request.POST['ytlink']
			link=ytlink
			link='https://www.youtube.com/embed/'+ link[link.index('=')+1:]+'?rel=0'
			song.title = title
			song.lyrics = lyrics
			song.link = link
			song.ytlink = ytlink
			try:
				song.save()
				messages.success(request, 'You just updated a Song')
			except:
				messages.warning(request,'An Error was encountered while updating your song')
			return redirect('songs-profile')
		else:
			audio = str(song.audio).split('/')[1]
			context={'object':song,'audio':audio}
			return render(request,'songs/updatesong.html',context)
	else:
		messages.warning(request,'You tried to update Song of another User.Conducting such tasks may result in deactivation of your account.')
		return redirect('songs-home')

class SongDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Song
    success_url = '/'

    def test_func(self):
        return str(self.get_object().composer) == str(self.request.user)

def list(request):
	songs = Song.objects.all()
	searchterm=''
	if request.method =='POST':
		if 'search' in request.POST:
			searchterm = request.POST['search']
			songs1=songs.filter(title__contains=searchterm)
			songs2=songs.filter(composer__contains=searchterm)
			songs3=songs.filter(featuring__contains=searchterm)
			songs=songs1|songs2|songs3
	songz = zip(songs,range(len(songs)+1)[1:])
	context = {'searchterm': searchterm,'songs':songz}
	return render(request, 'songs/listview.html', context) 

class SongDetailView(DetailView):
	model=Song
	fields=['title','img','lyrics','featuring','composer','album','link']
	template_name='songs/detailview.html'

def about(request):
	template = loader.get_template('songs/about.html')
	return HttpResponse(template.render({},request))





	# if 'search' in request.song:
	# 	searchterm=request.song['search']
	# 	songs=songs.filter(title__contains=searchterm)
	# context = {'searchterm': searchterm,
	# 			'songs':songs}
