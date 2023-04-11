from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from users.models import Profile, Follow
from django.contrib.auth.models import User
from posts.models import Post
from .forms import ReaderCreationForm, AuthorCreationForm, EditProfileForm


def index(request):
    """Home page."""
    return render(request, 'users/index.html')


def register(request):
    if request.method == "POST":
        form = ReaderCreationForm(request.POST)
        if form.is_valid():
            reader = form.save()
            login(request, reader.user)
            messages.success(request, f"Account created for {reader.username} successfully!")
            return redirect("users:index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information. Check all the requirements!")
            print(form.errors)
            # print(messages.error(request, form.errors))
    form = ReaderCreationForm()
    return render(request, template_name="users/register.html", context={"register_form": form})


def register_writer(request):
    if request.method == "POST":
        form = AuthorCreationForm(request.POST)
        if form.is_valid():
            writer = form.save()
            login(request, writer.user)
            messages.success(request, f"Account created for {writer.username} successfully!")
            return redirect("users:index")
        messages.error(request, form.errors)
    form = AuthorCreationForm()
    return render(request, template_name="users/register_writer.html", context={"register_form": form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('users:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name="users/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("users:index")


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    following = user.is_authenticated and user.following.exists()
    return render(request, 'users/profile.html', {'profile': profile, 'user': user, 'following': following})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.user.username, request.POST, request.FILES)
        if form.is_valid():
            about_me = form.cleaned_data['about_me']
            username = form.cleaned_data['username']
            image = form.cleaned_data['image']
            activity = form.cleaned_data['activity']
            country = form.cleaned_data['country']

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about_me = about_me
            profile.activity = activity
            profile.country = country
            if image:
                profile.image = image
            profile.save()
            return redirect('users:profile', username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def follow_index(request):
    user = request.user
    authors = user.follower.values_list('author', flat=True)
    posts_list = Post.objects.filter(author__id__in=authors)

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'users/follow.html', {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    user = request.user
    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
        return redirect('users:profile', username=username)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_unfollow(request, username):
    user = request.user
    if user:
        Follow.objects.get(user=user, author__username=username).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Exception('You cannot unfollow from yourself!')
