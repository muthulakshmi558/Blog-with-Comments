from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm, RegisterForm

# Registration
def register_view(request):
    if request.user.is_authenticated:
        return redirect('post-list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('post-list')
    else:
        form = RegisterForm()
    return render(request, 'blog_app/register.html', {'form': form})

# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('post-list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('post-list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog_app/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

class HomeView(TemplateView):
    template_name = 'blog_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Latest 4 posts
        context['latest_posts'] = Post.objects.order_by('-created_at')[:4]
        if self.request.user.is_authenticated:
                        context['latest_tasks'] = Task.objects.filter(user=self.request.user).order_by('-due_date')[:4]
        else:
                        context['latest_tasks'] = []
        return context
# Blog Views
class PostListView(ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

# Create, Update, Delete for posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog_app/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Add comment
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added!")
    return redirect('post-detail', slug=slug)

# Delete comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Comment deleted!")
    return redirect('post-detail', slug=comment.post.slug)
