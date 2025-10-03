from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from taggit.models import Tag

from .models import Post
from .forms import PostForm


# Post List
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


# Post Detail
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


# Post Create
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Post Update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Post Delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# 🔎 Search View
def post_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "blog/post_search.html", {"query": query, "results": results})


# 🏷️ Posts by Tag (Class-based)
class PostByTagListView(ListView):
    model = Post
    template_name = "blog/post_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return Post.objects.filter(tags__in=[self.tag]).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
