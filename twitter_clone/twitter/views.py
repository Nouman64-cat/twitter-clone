from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm
# Create your views here.
def home(request):
    tweets = Tweet.objects.all().order_by('-date_created')
    return render(request, 'home.html', {"tweets": tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must logged in first..."))
        return redirect('home')  

def user_profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        return render(request, 'profile.html', {"profile":profile}) 
    else:
        messages.success(request, ("You must logged in first..."))
        return redirect('home')
    
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # Set the user to the current user
            tweet.save()
            return redirect('home')  # Redirect after successful creation
    else:
        form = TweetForm()
    return render(request, 'create_tweet.html', {'form': form})