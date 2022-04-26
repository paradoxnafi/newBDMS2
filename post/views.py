from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from auth1.models import RegisterUser
from .models import Post, Comment
from .forms import PostForm, CommentForm

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def home(request):

    post = Post.objects.order_by('-created_at')
    # pagination
    p = Paginator(post, 5) # Choose how many post will display
    page = request.GET.get('page', 1)
    try:
        paginated_post = p.page(page)
        # paginated_post = p.get_page(page)
    except EmptyPage:
        paginated_post = p.page(1)


    return render(request, 'post/home.html', {
#        'post': post,
        'post': paginated_post,
        })


def createpost(request):
    if request.method == 'GET':
        return render(request, 'post/createpost.html', {'form': PostForm})
    else:
        form = PostForm(request.POST)
        newform = form.save(commit=False)
        newform.save()
        return redirect('home')


# def view_single_post(request, post_id): 
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
            post_id = post.id # (1) this line 
            messages.success(request, "Post updated successfully.")
            return redirect(f'/posts/view/{post_id}') # (2) and this line fixed after edit redirect issue

    return render(request, "post/edit_post.html", {
        'post': post,
        'form': form
    })

@login_required(login_url='loginUser')
def my_posts(request):

    post = Post.objects.order_by('-created_at')
    return render(request, 'post/my_post.html', {
        'post': post,
        })
    

@login_required(login_url='loginUser')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('home')

@login_required(login_url='loginUser')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_id = comment.post.id
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(f'/posts/view/{post_id}')



# Create your views here.
@login_required
def generatePDF(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Add some text
    lines = [
        'line 1',
        'line 2',
        'line 3'
    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='post_report.pdf')
