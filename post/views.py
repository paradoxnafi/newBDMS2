from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404  
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
import datetime
from auth1.models import RegisterUser, Notification
from .models import Post, Comment
from .forms import PostForm, CommentForm

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def home(request):

    post = Post.objects.filter(admin_approved=True).order_by('-created_at')
    # pagination
    p = Paginator(post, 5) # Choose how many post will display
    page = request.GET.get('page', 1)
    try:
        paginated_post = p.page(page)
    except EmptyPage:
        paginated_post = p.page(1)

    return render(request, 'post/home.html', {
        'post': paginated_post,
        })


def createpost(request):
    if request.method == 'GET':
        return render(request, 'post/createpost.html', {'form': PostForm})
    else:
        form = PostForm(request.POST)
        newform = form.save(commit=False)
        newform.save()
#        print(newform.pk)
        asking_blood_group = newform.blood_group

        users = RegisterUser.objects.filter(blood_group=asking_blood_group).exclude(id=request.user.id)
        message = f"{request.user} needs {asking_blood_group},"
        notification = Notification.objects.create(message=message, context=newform.pk)
        notification.receiver.set(users)

        messages.success(request, "Your post is under review by an admin. It will be visible to everyone shortly.")
        # Send email for creating new post.
        # subject = "Your post is under review by and admin"
        # message = f" Hey {request.user.name}, your post is under review by an admin. It will be visible to everyone shortly. Click http://127.0.0.1:8000/posts/view/{newform.pk} to edit your post."
        # recipient = f"{request.user.email}"
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [recipient],
        #     fail_silently = False
        # )

        return redirect('home')

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
            # messages.success(request, "Comment added successfully.")
            # Send email for comments
            # subject = f"{request.user.name} commented on your post"
            # post_author = RegisterUser.objects.get(pk=post.author.pk)
            # message = f" Hey {post_author.name}, {request.user.name} commented on your post. Click http://127.0.0.1:8000/posts/view/{post_id} to visit your post."
            # recipient = f"{post.author.email}"
            # send_mail(
            #     subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [recipient],
            #     fail_silently = False
            # )
        
        user = RegisterUser.objects.filter(pk=post.author.id)
        if request.user.id != user[0].id: 
            message = f"{request.user} commented on your post"
            notification = Notification.objects.create(message=message, context=post_id)
            notification.receiver.set(user)

    resetForm = CommentForm()
    updatedComment = Comment.objects.order_by('-created_at')
    # Calculate age of request.user
    profile = RegisterUser.objects.get(id=request.user.id)
    born = request.user.date_of_birth
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    # Calculate last donation since for request.user
    last_donation_date = request.user.last_donated
    if last_donation_date != None:
        today = date.today()
        delta = today - last_donation_date
        days_since = delta.days
    else:
        days_since = ""

    return render(request, "post/single_post.html", {
        'post': post,
        'form': resetForm,
        'comment': updatedComment,
        'profile': profile,
        'age': age,
        'days': days_since,
    })


def view_user(request, user_id):
    context = {}
    profile = RegisterUser.objects.get(id=user_id)
    context['profile'] = profile
    print(user_id)
  
    born = profile.date_of_birth
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    return render(request, 'auth1/profile.html', {
        'profile': profile,
        'age': age,
    })

@login_required(login_url='loginUser')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.is_resolved != True:
        form = PostForm(instance=post)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                form.save()
                donated_by = request.POST.getlist('donated_by')
                
                for item in donated_by:
                    user = RegisterUser.objects.get(pk=item)
                    user.donation_count += 1
                    user.last_donated = (timezone.now())
                    print(user.last_donated, user.donation_count)
                    user.save()

                post_id = post.id # (1) this line 
                # messages.success(request, "Post updated successfully.")
                return redirect(f'/posts/view/{post_id}') # (2) and this line fixed after edit redirect issue

        return render(request, "post/edit_post.html", {
            'post': post,
            'form': form
        })
    else:
        raise Http404

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
    # messages.success(request, "Post deleted successfully.")
    return redirect('home')

@login_required(login_url='loginUser')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_id = comment.post.id
    comment.delete()
    # messages.success(request, "Comment deleted successfully.")
    return redirect(f'/posts/view/{post_id}')



# Create your views here.
@login_required
def generatePDF(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    
    # Add to report
    lines = []
    number_of_users = RegisterUser.objects.count()
    number_of_posts = Post.objects.count()
    number_of_resolved_posts = Post.objects.filter(is_resolved = True).count()
    number_of_comments = Comment.objects.count()
    print(number_of_posts)

    lines.append(f'Total user count:          {number_of_users}')
    lines.append(f'Total post count:          {(number_of_posts)}')
    lines.append(f'Resolved post count:   {number_of_resolved_posts}')
    lines.append(f'Total comment count:  {number_of_comments}')
    lines.append(' ')
    lines.append(f'Generated from Django Admin at {datetime.datetime.now()} by "{request.user}"')

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    if request.user.is_admin == True:
        return FileResponse(buf, as_attachment=True, filename='System_Report.pdf')
    else:
        return HttpResponse("<p> You are not authorization to view this page")

# send notification and email after post is approved
# def if_post_approved(request):
    # users = RegisterUser.objects.filter(blood_group=asking_blood_group).exclude(id=request.user.id)
    # message = f"{request.user} needs {asking_blood_group},"
    # notification = Notification.objects.create(message=message, context=newform.pk)
    # notification.receiver.set(users)

    # Send email for creating new post.
    # subject = "Your post is under review by and admin"
    # message = f" Hey {request.user.name}, your post is under review by an admin. It will be visible to everyone shortly. Click http://127.0.0.1:8000/posts/view/{newform.pk} to edit your post."
    # recipient = f"{request.user.email}"
    # send_mail(
    #     subject,
    #     message,
    #     settings.EMAIL_HOST_USER,
    #     [recipient],
    #     fail_silently = False
    # )
