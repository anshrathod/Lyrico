from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from songs.models import Song
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

def home(request):
	if request.method =='song':
		songs = Song.objects.all()
		searchterm=''
		if 'search' in request.song:
			searchterm = request.song['search']
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

	def form_valid(self,form):
		self.request.user in [form.instance.composer,form.instance.featuring]
		return super().form_valid(form)

	def test_func(self):
		song=self.get_object()
		if self.request.user in [song.composer,song.featuring]:
			return True
		return False

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
	if request.method =='song':
		if 'search' in request.song:
			searchterm = request.song['search']
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
	if request.method =='song':
		if 'search' in request.song:
			searchterm = request.song['search']
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