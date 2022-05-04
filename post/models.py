from django.db import models
from author.decorators import with_author

BLOOD_GROUPS = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

@with_author
class Post(models.Model):
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250)
    blood_group = models.CharField(max_length=8, choices=BLOOD_GROUPS)
    required_bags = models.PositiveIntegerField()
    deadlineDate = models.DateField()
    deadlineTime = models.TimeField()
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False, blank=True)
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.author) + ", " + str(self.blood_group) + ", " + str(self.address)

@with_author
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank="True")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + " commented at " + str(self.post.author) + "'s post" + ", " + str(self.body)
        