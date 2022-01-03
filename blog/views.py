from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Profile
from .forms import ProfileForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import Q


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    
   

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class AddPostView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'post_form.html'
    fields = '__all__'

class UpdatePostView(UpdateView, LoginRequiredMixin):
    model = Post
    template_name = 'update.html'
    fields = ['title', 'body', 'category', 'id']

class DeletePostView(DeleteView, LoginRequiredMixin):
     model = Post
     template_name = 'delete.html'
     success_url = reverse_lazy('home')


class UserRegisterView(FormView):
    template_name = 'registration.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)
        
        

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(UserRegisterView, self).get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)

    return render(request,'category.html', {'cats':cats, 'category_posts':category_posts})
    


class AddCommentView(CreateView, LoginRequiredMixin):
    model = Comment
    template_name = 'comment.html'
    fields = '__all__'

    success_url = reverse_lazy('home')

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile_page.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        
        return context

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'create_profile.html'
    fields = ['avatar', 'bio', 'email',  'twitter']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('home')

class EditProfileView(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class=ProfileForm
    
    success_url = reverse_lazy('home')
    