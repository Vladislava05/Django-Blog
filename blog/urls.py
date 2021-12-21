from django.urls import path
from .views import BlogListView, BlogDetailView, AddPostView, CustomLoginView, UpdatePostView, DeletePostView, UserRegisterView, CategoryView, AddCommentView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post_form/', AddPostView.as_view(), name='post_form'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('registration/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('post/update/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]