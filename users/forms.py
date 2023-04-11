from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Reader, Author


class ReaderCreationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Reader
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        super().clean()
        user: User = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password1'])

        reader = Reader.objects.create(
            user=user,
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )

        if commit:
            user.save()
        return reader


class AuthorCreationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Author
        fields = ('username', 'email', 'password1', 'password2',
                  'company', 'activity', 'blog')

    def save(self, commit=True):
        user: User = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password1'])
        author = Author.objects.create(
            user=user,
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            company=self.cleaned_data['company'],
            activity=self.cleaned_data['activity'],
            blog=self.cleaned_data['blog']
        )
        if commit:
            user.save()
        return author


class EditProfileForm(forms.Form):
    username = forms.CharField()
    activity = forms.CharField(max_length=50)
    about_me = forms.CharField(widget=forms.Textarea())
    country = forms.CharField(max_length=50)
    image = forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'A user with that username already exists.')
        return username




