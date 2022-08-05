from django.urls import path


from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post/new/', views.PostCreateView.as_view(), name='new'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('like/<int:pk>', views.LikeView, name='like'),
    path('api/', views.getData, name='message-list'),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', views.CreateMessage.as_view(), name='create-message'),
]