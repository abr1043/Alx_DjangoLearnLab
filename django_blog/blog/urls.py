from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # ✅ Search
    path("search/", views.post_search, name="post-search"),

    # ✅ Tags with slug + Class-based view
    path("tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="post-by-tag"),
]
