from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from songs.models import Song
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

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
		context = {'searchterm': searchterm,'songs':songs}
		return render(request, 'songs/listview.html', context) 
	return render(request,'songs/base.html')

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
	context = {'searchterm': searchterm,'songs':songs}
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
	context = {'searchterm': searchterm,'songs':songs}
	return render(request, 'songs/boxlistview.html', context) 

class SongDetailView(DetailView):
	model=Song
	fields=['title','img','lyrics','featuring','composer','album','link']
	template_name='songs/detailview.html'

def login(request, method = [ 'POST']):
	if request.method=='POST':
		print('qwerty')
		username=request.POST['username']
		password=request.POST['password']
		if username == 'anshrathod':
			if password == 'testing123':
				return redirect('songs-add')
		return render(request,'songs/login.html')

	else :
		print('asdf')
		return render(request,'songs/login.html')

@login_required
def addsong(request):
	if request.method=='POST':
		print(request.POST)
		title=request.POST['title']
		lyrics=request.POST['lyrics']
		composer=request.POST['composer']
		featuring=request.POST['featuring']
		album=request.POST['album']
		img=request.POST['img']
		link=request.POST['link']
		featuring = ': '+ featuring
		link='https://www.youtube.com/embed/'+ link[link.index('=')+1:]+'?rel=0'
		song = Song(title=title,lyrics=lyrics,composer=composer,featuring=featuring,album=album,img=img,link=link)
		song.save()
		return render(request,'songs/addsong.html')		
	else:
		return render(request,'songs/addsong.html')

def about(request):
	template = loader.get_template('songs/about.html')
	return HttpResponse(template.render({},request))






	# if 'search' in request.POST:
	# 	searchterm=request.POST['search']
	# 	songs=songs.filter(title__contains=searchterm)
	# context = {'searchterm': searchterm,
	# 			'songs':songs}