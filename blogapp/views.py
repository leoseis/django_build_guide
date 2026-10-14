from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):

        posts = Post.objects.all().order_by("-created_at")

        return render(
            request,
            "blogapp/post_list.html",
            {"posts": posts}
        )


def post_detail(request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        return render(
            request,
            "blogapp/post_detail.html",
            {"post": post}
        )
