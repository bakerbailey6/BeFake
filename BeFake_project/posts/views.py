from urllib import request
from xml.etree.ElementTree import Comment
from django.dispatch import receiver
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from rest_framework import viewsets, permissions
from .models import Comments, Post, MessageModel, ThreadModel
from .forms import CommentForm, ThreadForm, MessageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import MessageSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q




class PostListView(ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):

        return Post.objects.order_by('-created')



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self , *args, **kwargs):
        data = super().get_context_data(**kwargs)
        connected_comments = Comments.objects.filter(CommentPost=self.get_object())
        number_of_comments = connected_comments.count()
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['liked'] = liked
        return data
    
    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            print('Reached here')
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None

            

            new_comment = Comments(content=content , author = self.request.user , CommentPost=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts:home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('posts:detail', args=[str(pk)]))


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('posts:thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('posts:thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('posts:thread', pk=thread.pk)
        except:
            return redirect('posts:create-thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return redirect('posts:thread', pk=pk)




@api_view(['GET'])
def getData(request):
    user = User.objects.all()
    messages = MessageModel.objects.all()
    message_serializer = MessageSerializer(messages, many=True)
    serializer = UserSerializer(user, many=True)
    context={}
    context['users'] = serializer.data
    context['messages']=message_serializer.data
    return Response(context)

            