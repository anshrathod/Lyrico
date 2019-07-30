from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)

from songs.models import Song
from users.models import Profile


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

class SongUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Song
	fields=['title','lyrics','img']
	# def form_valid(self,form):
	# 	self.request.user in [form.instance.composer,form.instance.featuring]
	# 	return super().form_valid(form)

	def test_func(self):
		# song=self.get_object()
		# if self.request.user in [song.composer,song.featuring]:
		return True
		# return False
def updatesong(request,pk):
	if request.method == 'POST':
		song = Song.objects.get(id=pk)
		title = request.POST['title']
		lyrics = request.POST['lyrics']
		print(request.FILES['audio'])
		if request.FILES['image']:
			image = request.FILES['image']
			song.img = image
		if request.FILES['audio']:
			audio = request.FILES['audio']
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
		song = Song.objects.get(id=pk)
		context={'object':song}
		return render(request,'songs/updatesong.html',context)

class SongDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Song
    success_url = '/'

    def test_func(self):
        # print(self.get_object())
        # if self.request.user == self.get_object().composer:
        return True
        # return False


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

def box(request):
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
	return render(request, 'songs/boxlistview.html', context) 

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
