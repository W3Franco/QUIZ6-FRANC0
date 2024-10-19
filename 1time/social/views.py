from django.shortcuts import render
from django.views import View
from django.contrib import messages  # Import messages for feedback
from django.core.exceptions import ValidationError  # Import ValidationError
from .models import Post
from .forms import PostForm

class PostListView(View):
    def get(self, request, *args, **kwargs):
        # Fetch only the latest 3 posts
        posts = Post.objects.all().order_by('-created_on')[:3]  # Limit to 3 posts
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        # Limit posts to the latest 3 after a new post is created
        posts = Post.objects.all().order_by('-created_on')[:3]  # Limit to 3 posts
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user

            try:
                new_post.save()  # Attempt to save the new post
                messages.success(request, "Post created successfully!")  # Success message
            except ValidationError as e:
                messages.error(request, "One Post Only")  # Display the error message

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)