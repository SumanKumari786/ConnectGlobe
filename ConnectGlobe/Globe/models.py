from django.db import models
from django.db.models import Model
from django.contrib.auth.models import auth, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
# Create your models here.
from django.utils.timezone import now


class Feedback(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    message = models.TextField(max_length=225)
    date = models.DateField(auto_now_add=True)


class Profilee(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profilee(sender, instance, created, **kwargs):
    if created:
        Profilee.objects.create(user=instance)
        instance.profilee.save()


class MyProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', null=True)


@receiver(post_save, sender=User)
def update_my_profile(sender, instance, created, **kwargs):
    if created:
        MyProfile.objects.create(user=instance)
        instance.myprofile.save()


class Post(models.Model):
    objects = models.Manager()
    CATEGORY_CHOICES = (
        ("Django", "Django"),
        ("Python", "Python"),
        ("Java", "Java"),
        ("C++", "C++"),
        ("C", "C"),
        ("Database", "Database"),
    )
    name = models.ForeignKey(User, on_delete=models.PROTECT, related_name='name')
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(choices=CATEGORY_CHOICES, default='Django', max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    file = models.FileField(upload_to='project_files', null=True, blank=True)
    slug = models.CharField(max_length=130)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})


class PostComment(models.Model):
    objects = models.Manager()
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('PostComment', on_delete=models.CASCADE, null=True, related_name='replies')
    timestamp = models.DateTimeField(default=now)


class Discussion(models.Model):
    objects = models.Manager()
    text = models.TextField()
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return 'Discussion #{}'.format(self.id)

    class Meta:
        verbose_name_plural = 'entries'
