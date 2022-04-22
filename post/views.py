from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth1.models import RegisterUser
from .models import Post, Comment
from .forms import PostForm, CommentForm

def home(request):

    post = Post.objects.order_by('-created_at')
    return render(request, 'post/home.html', {'post': post})

def createpost(request):
    if request.method == 'GET':
        return render(request, 'post/createpost.html', {'form': PostForm})
    else:
        form = PostForm(request.POST)
        newform = form.save(commit=False)
        newform.save()
        return redirect('home')


# def view_single_post(request, post_id): # @shuvro
#     if request.method == 'GET':
#         post = Post.objects.get(pk=post_id)
#         return render(request, 'post/single_post.html', { 'post': post})

def single_post(request, post_id):
    form = CommentForm()
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment.objects.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
    resetForm = CommentForm()
    updatedComment = Comment.objects.order_by('-created_at')
    return render(request, "post/single_post.html", {
        'post': post,
        'form': resetForm,
        'comment': updatedComment,
    })

def view_user(request, user_id):
    context = {}
    profile = RegisterUser.objects.get(id=user_id)
    context['profile'] = profile
    print(user_id)
    return render(request, 'auth1/profile.html', context)

@login_required(login_url='loginUser')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('home')

    return render(request, "post/edit_post.html", {
        'post': post,
        'form': form
    })

@login_required(login_url='loginUser')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('home')