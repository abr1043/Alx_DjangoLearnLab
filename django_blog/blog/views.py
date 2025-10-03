from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Post

# ✅ List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]

# ✅ Detail view
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

# ✅ Create new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "tags"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ✅ Update post (only author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "tags"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ✅ Delete post (only author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post-list")
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ✅ Search functionality
def post_search(request):
    query = request.GET.get("q")
    results = Post.objects.all()

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, "blog/post_search.html", {"results": results, "query": query})

# ✅ Filter by tag
def post_by_tag(request, tag_name):
    results = Post.objects.filter(tags__name__icontains=tag_name)
    return render(request, "blog/post_by_tag.html", {"results": results, "tag": tag_name})
