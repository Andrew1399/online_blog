from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Reader(models.Model):
    """
    A simple model of a reader who learns information
    in the blog.
    """
    class Meta:
        verbose_name = _('Reader')
        verbose_name_plural = _('Readers')

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reader'
    )
    username = models.CharField(_('username'), max_length=50, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"Reader {self.username} "


class Author(models.Model):
    """A model of a writer who can create own posts
    and own content.
    """
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='author'
    )

    username = models.CharField(_('username'), max_length=50, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    company = models.CharField(_('company'), max_length=60, blank=True)
    activity = models.CharField(_('activity'), max_length=70, blank=True)
    blog = models.CharField(_('blog'), max_length=50, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username}"


class Profile(models.Model):
    about_me = models.TextField()
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    activity = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def count_posts(self):
        return self.user.author.posts.count()

    def count_comments(self):
        return self.user.comments.count()

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    # user who follow
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    # the user being subscribed to
    author = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'author'),)

    def save(self, **kwargs):
        if self.user == self.author:
            raise ValueError('Cannot follow yourself')
        super(Follow, self).save(**kwargs)

    def __str__(self):
        return f"Follower {self.user}, author: {self.author}"

