from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from Globe.models import Feedback, MyProfile, Post, PostComment
from Globe.tokens import account_activation_token

from .forms import *
from django.contrib.auth.forms import PasswordChangeForm

from django.core.paginator import Paginator
# Create your views here.


def connect_login(request):
    if request.method == 'POST':
        n = request.POST['name']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=n, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('/view_status')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/Register')
    else:
        return render(request, "Globe/login.html")


def logout(request):
    auth.logout(request)
    return redirect('/index')


def connect_register(request):
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        un = request.POST['usname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        em = request.POST['email']

        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request, 'Username already Taken')
                print("Username Taken")
                return redirect('/Register')
            elif User.objects.filter(email=em).exists():
                messages.info(request, 'Email already Taken')
                print("Username Taken")
                return redirect('/Register')
            else:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=un, password=pass1, email=em, )
                user.save()
                # MyProfile.objects.create(user=user)

                current_site = get_current_site(request)
                subject = 'Activate Your ConnectGlobe Account'
                message = render_to_string('Globe/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                #send_mail(
                    #    "Hello User",
                    #   "Welcome to Email Confirmation",
                    #  "btesinstitute74@gmail.com",
                    # [em],
                    #fail_silently=False,
                 #)
                send_mail(
                        subject,
                        message,
                        'btesinstitute74@gmail.com',
                        [em],
                        fail_silently=False,
                    )

                messages.success(request, 'Please Confirm your email.')
                return redirect('/email_confirm_msg')
        else:
            messages.info(request, 'Password does not match')

        return redirect('/Register')

    else:
        return render(request, "Globe/register.html")


def index(request):
    return render(request, "Globe/index.html")


def about(request):
    return render(request, "Globe/about.html")


@login_required(login_url='/login/')
def view_status(request):
    posts = Post.objects.filter(name=request.user)
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')  # page variable is used to get page number that we passing in view
    # ?page=2
    posts = paginator.get_page(page)  # to access the items in page use get_page method
    params = {'posts': posts}
    return render(request, "Globe/myposts.html", params)


class PostListView(ListView):
    model = Post
    template_name = 'Globe/view_status.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post


def continuepost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = PostComment.objects.filter(post=post, reply=None)

    if request.method == 'POST':
        commentform = CommentForm(request.POST or None)
        if commentform.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_sno')
            comment_qs = None
            if reply_id:
                comment_qs = PostComment.objects.get(sno=reply_id)
            postcomment = PostComment.objects.create(post=post, user=request.user, comment=comment, reply=comment_qs)
            postcomment.save()
    else:
        commentform = CommentForm()

    context = {'post': post, 'comments': comments, 'commentform': commentform}
    return render(request, "Globe/continue.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post
    fields = ['title', 'category', 'slug', 'content', 'file']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)


def search(request):
    query = request.GET['query']
    if len(query) > 50:
        posts = Post.objects.none()
    else:
        postsTitle = Post.objects.filter(title__icontains=query)
        postsCategory = Post.objects.filter(category__icontains=query)
        posts = postsTitle.union(postsCategory)
    if posts.count() == 0:
        messages.warning(request, 'No Search Results, Please Refine Your Query')
    params = {'posts': posts, 'query': query}
    return render(request, "Globe/search.html", params)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'slug', 'content', 'file']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/view_status'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False

@login_required(login_url='/login/')
def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        msg = request.POST.get('message', '')
        feedback = Feedback(name=name, email=email, message=msg)
        feedback.save()
        messages.info(request, 'Thanks for your Valuable Feedback')
    return render(request, "Globe/feedback.html")


def email_confirm_msg(request):
    return render(request, "Globe/email_confirm_msg.html")


def confirmed_email(request):
    return render(request, "Globe/confirmed_email.html")


def dev_team(request):
    return render(request, "Globe/development_team.html")


@login_required(login_url='/login/')
def view_profile(request):
    return render(request, "Globe/View_Profile.html")


@login_required(login_url='/login/')
def update_profile(request):
    if request.method == 'POST':

       u_form = UserUpdate(request.POST, instance=request.user)
       p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.myprofile)

       if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, 'Your Profile is updated Successfully')
          return redirect('/view_profile')
       else:
           messages.error(request, 'Something wrong:')
    else:
       u_form = UserUpdate(instance=request.user)
       p_form = ProfileUpdate(instance=request.user.myprofile)
    context = {
       'u_form': u_form,
       'p_form': p_form
    }
    return render(request, "Globe/Update_Profile.html", context)


@login_required(login_url='/login/')
def changePass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            messages.success(request, 'Your password change successfully')
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form': form,
    }
    return render(request, "Globe/changePass.html", params)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            #uid = force_text(urlsafe_base64_decode(uidb64))
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profilee.email_confirmed = True
            user.save()
            #login(request, user)
            messages.success(request, 'Your account have been confirmed. Please Login')
            print("confirmed", user.is_active)
            return render(request, 'Globe/confirmed_email.html')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return render(request, 'Globe/thanks.html')
