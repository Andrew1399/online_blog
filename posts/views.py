from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
    DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from posts.models import Post, Comment, Category
from posts.forms import CommentForm


class HomeView(ListView):
    template_name = 'posts/post_page.html'
    queryset = Post.objects.all()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


def CategoryView(request, cats):
    category = get_object_or_404(Category, slug=cats)
    category_posts = Post.objects.filter(categories=category)
    return render(request, 'posts/categories.html', {'category': category, 'category_posts': category_posts})


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk, slug=slug)
        # following = (self.request.user.is_authenticated
        #     and post.author.following.filter(user=self.request.user.author).exists())
        get_likes = get_object_or_404(Post, id=self.kwargs['pk'])
        count_likes = get_likes.count_likes()

        liked = False
        if get_likes.likes.filter(id=self.request.user.id).exists():
            liked = True

        comments = post.comment_set.all()
        context['post'] = post
        context['categories'] = Category.objects.all()
        context['comments'] = comments
        # context['following'] = following
        context['count_likes'] = count_likes
        context['liked'] = liked
        context['form'] = form

        return context


    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                content=content, post=post, author=request.user)

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)
        return self.render_to_response(context=context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image', 'tags']

    def get_success_url(self):
        messages.success(self.request, 'Your post has been created successfully!')
        return reverse_lazy('posts:post_page')

    def form_valid(self, form):
        try:
            obj = form.save(commit=False)
            form.instance.author = self.request.user.author
            obj.slug = slugify(form.cleaned_data['title'])
            obj.save()
            return super().form_valid(form)
        except:
            return HttpResponse(f"<h1>You cannot create posts! Sign up like an author!<h1>")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image', 'tags']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update
        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully!'
        )
        return reverse_lazy('posts:post_page')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user.author)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully!'
        )
        return reverse_lazy('posts:post_page')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user.author)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SearchPostView(ListView):
    model = Post
    template_name = 'posts/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        return object_list

