from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from blog.forms import CreateBlog
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'index.html', {"blogs": blogs})

@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'GET':
        form = CreateBlog(instance=blog)
        return render(request, 'blog_detail.html', {'blog': blog, 'form': form})
    else:
        try:
            form = CreateBlog(request.POST, instance=blog)
            form.save()
            return redirect('blog_detail')
        except ValueError:
            return render(request, 'blog_detail.html', {'blog': blog, 'form': form, 'error': 'Bad Info'})


@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def deleteblog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('index')
