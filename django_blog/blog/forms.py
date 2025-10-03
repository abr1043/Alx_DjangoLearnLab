from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    # optional helper field for native-tag input
        class Meta:
        model = Post
        fields = ["title", "content", "tags"] 

    class Meta:
        model = Post
        fields = ["title", "content"]  # tags handled separately

    def __init__(self, *args, **kwargs):
        # If editing an instance, prefill tags_field
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        if instance:
            self.fields["tags_field"].initial = ", ".join([t.name for t in instance.tags.all()])

    def save(self, commit=True):
        post = super().save(commit=commit)
        tags_str = self.cleaned_data.get("tags_field", "")
        # normalize and create tags
        tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
        # replace post tags with current list
        post.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={"name": name})
            # get_or_create with case-insensitive: handle both ways:
            if not tag:
                tag = Tag.objects.get(name__iexact=name)
            post.tags.add(tag)
        return post
