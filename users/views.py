from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from songs.models import Song

from .models import Profile
from .signup import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, ('{},Just Logged In!'.format(username)))
				return redirect('songs-home')
			else:
				messages.warning(request,'Your account has been deactivated.')
				return render(request, 'users/login.html')
		else:
			messages.warning(request,'The account details entered were wrong.')
			return render(request, 'users/login.html')
	return render(request, 'users/login.html')
	

def signup(request):
	if request.method=='POST':
		user = UserRegisterForm(request.POST)
		if user.is_valid():
			username = user.cleaned_data.get('username')
			mail=user.cleaned_data.get('email')
			if valid_email(mail):
				user.save()
				messages.success(request, ('Account has been created for {}! Please Fill the details to build up your Profile.'.format(username)))
				useracc=User.objects.get(username=username)
				profile=Profile(user = useracc)
				profile.save()
				login(request,useracc)
			else:
				messages.warning(request,'Your account couldn\'t be created...')
				return redirect('songs-signup') 
			return redirect('songs-addprofile')
	else:
		user = UserRegisterForm()
	return render(request,'users/register.html',{'form':user})

# def register(request):
# 	if request.method == 'POST':
# 		fname = request.POST['fname']
# 		lname = request.POST['lname']
# 		username = request.POST['username']
# 		email = request.POST['email']
# 	return render(request,'users/signup.html',{})

def valid_email(mail):
    domains = ['somaiya.edu',
               'gmail.com' ,]
    user_domain = mail.split('@')[1]
    if user_domain in domains:
        return True
    return False

def changepass(request):
	pass


@login_required
def addsong(request):
	if request.method=='POST':
		title=request.POST['title']
		lyrics=request.POST['lyrics']
		composer=request.user.username
		featuring=request.POST['featuring']
		album=request.POST['album']
		img=request.FILES['img']
		link=request.POST['link']
		genre=request.POST['genre']
		genre = genre.upper() 
		audio=request.FILES['audio']
		ytlink=link
		link='https://www.youtube.com/embed/'+ link[link.index('=')+1:]+'?rel=0'
		song = Song(title=title,lyrics=lyrics,composer=composer,featuring=featuring,album=album,img=img,link=link,ytlink=ytlink,audio=audio,genre=genre)
		song.save()
		return render(request,'users/display_profile.html')		
	else:
		return render(request,'songs/addsong.html')

def logout_user(request):
	logout(request)
	messages.warning(request,'You have successfully logged out.')
	return redirect('songs-home')

@login_required
def profile(request):
	mysongs = list()
	songs = Song.objects.all()
	username = request.user.username
	for song in songs:
		if song.composer == username or song.featuring == username:
			mysongs.append(song)
	size = len(mysongs)
	context = {'size': size,'songs':mysongs} 
	return render(request,'users/display_profile.html',context)

def addprofile(request):
	if request.user.profile.image:
		return redirect('songs-profile')
	else:
		if request.method =="POST":
			username=request.POST.get('username')
			print(username)
			users = User.objects.filter(username=username)
			user = users[0] 
			profile=Profile.objects.get(user=user)
			profile.fname=request.POST['fname']
			profile.lname=request.POST['lname']
			profile.gender=request.POST['gender']
			profile.age=request.POST['age']
			profile.bio=request.POST['bio']
			profile.image=request.FILES['pic']
			profile.save()
		else:
			return render(request,'users/addprofile.html')
		return render(request,'songs/base.html')

def update(request):
		profile = request.user
		mysongs = list()
		a=0
		userprofile = Profile.objects.get(user=profile)
		if request.method == 'POST':
			print('tp')
			try:
				if request.POST['fname']!=profile.first_name:
					fname = request.POST['fname']
					a+=1
				else:
					fname=profile.first_name
				if request.POST['lname']!=profile.last_name:
					lname = request.POST['lname']
					a+=1
				else:
					lname=profile.last_name
				if request.POST['gender']!=userprofile.gender:
					gender = request.POST['gender']
					a+=1
				else:
					gender=userprofile.gender
				if request.POST['age']!=userprofile.age:
					age = request.POST['age']
					a+=1
				else:
					age=userprofile.age
				if request.POST['bio']!=userprofile.bio:
					bio = request.POST['bio']
					a+=1
				else:
					bio=userprofile.bio
				if request.FILES['pic']!=userprofile.image:
					pic = request.FILES['pic']
					a+=1
				else:
					pic=userprofile.image
				profile.first_name = fname
				profile.last_name = lname
				userprofile.gender=gender
				userprofile.age=age
				userprofile.bio=bio
				userprofile.image=pic
				userprofile.save()
				profile.save()
				if a>1:
					messages.success(request, 'Your Account has been updated!')
			except:
				messages.warning(request,'An Error Occured while updating your profile.')
			finally:
				return redirect('songs-profile')
		songs = Song.objects.all()
		username = profile.username
		for song in songs:
			if song.composer == username or song.featuring == username:
				mysongs.append(song)
		context={
			'songs':mysongs,
			'profile':userprofile
		}
		return render(request,'users/profile.html',context)
