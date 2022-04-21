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

    return render(request, "post/single_post.html", {
        'post': post,
        'form': form,
        'comment': comment,
    })

# def view_comments(request):
#     comment = Comment.objects.order_by('-created_at')
#     return render(request, 'post/single_post.html', {'comment': comment})


def view_user(request, user_id):
    context = {}
    profile = RegisterUser.objects.get(id=user_id)
    context['profile'] = profile
    print(user_id)
    return render(request, 'auth1/profile.html', context)


# def view_comments(request):
#     comment = Comment.objects.order_by('created_at')
#     return render(request, 'post/single_post.html', {'comment': comment})








# @login_required(login_url='loginUser')
# def edit_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(instance=feed)

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=feed)

#         if form.is_valid():
#             form.save()
#             messages.success(request, "Post updated successfully.")
#             return redirect('home')

#     return render(request, "post/craetepost.html", {
#         'feed': feed,
#         'form': form
#     })


# @login_required(login_url='login')
# def delete_post(request, pk):
#     feed = get_object_or_404(Post, pk=pk)
#     feed.delete()
#     messages.success(request, "Post deleted successfully.")
