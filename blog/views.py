from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Profile
from .forms import ProfileForm, CommentForm, PostForm
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
   
class SearchResultsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'search_results.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = context['posts'].filter(author=self.request.user)
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['posts'] = context['posts'].filter(title__icontains=search_input)
        context['search_input'] = search_input

        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_dislikes = stuff.total_dislikes()
        context['total_dislikes'] = total_dislikes
        context['total_likes'] = total_likes
        return context


class AddPostView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'post_form.html'
    form_class=PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddPostView, self).form_valid(form)


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

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))  
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))  
    post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


class AddCommentView(CreateView, LoginRequiredMixin):
    model = Comment
    template_name = 'comment.html'
    form_class = CommentForm
    
    def form_valid(self, form):
         form.instance.post_id = self.kwargs['pk']
         form.instance.name = self.request.user
         return super(AddCommentView, self).form_valid(form)
    

        
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
    