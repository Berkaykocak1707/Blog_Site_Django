from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .models import Blog, Comment, Reply,Category
from django.db.models import Q 
from .forms import CommentForm
from django.contrib import messages

def index(request):
    # Öne çıkarılan blog gönderisini al
    featured_post = Blog.objects.filter(featured=True).first()
    
    # Eğer bir featured post varsa, onu hariç tüm gönderileri al
    if featured_post:
        all_other_posts = Blog.objects.exclude(id=featured_post.id)
    else:
        # Eğer öne çıkarılan bir post yoksa, tüm gönderileri al
        all_other_posts = Blog.objects.all()

    # Sayfalama için Paginator sınıfını kullan
    paginator = Paginator(all_other_posts, 4)  # Her sayfada 4 gönderi olacak
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'featured_post': featured_post,
        'page_obj': page_obj
    }
    return render(request, 'index.html', context)


def blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    # Yalnızca ana yorumları getir
    main_comments = Comment.objects.filter(blog=blog).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = request.POST.get('comment')
            name = request.POST.get('name')
            parent_id = request.POST.get('comment_id')

            if parent_id:  # Eğer bir yoruma yanıt veriliyorsa
                parent_comment = Comment.objects.get(id=parent_id)
                reply = Reply(comment=parent_comment, name=name, reply=comment_text)
                reply.save()
            else:  # Eğer ana yorum ekleniyorsa
                comment = Comment(blog=blog, name=name, comment=comment_text)
                comment.save()

            messages.success(request, 'Yorumunuz başarıyla eklendi!')
            return redirect('blog_detail', slug=blog.slug)
        else:
            messages.error(request, 'Formunuzda bir hata var. Lütfen girişlerinizi kontrol edin.')
    else:
        comment_form = CommentForm()

    context = {
        'blog': blog,
        'main_comments': main_comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blog_list = Blog.objects.filter(categories=category).order_by('-date')  # '-date' ile en yeni gönderilerin önce gelmesini sağlar.

    # Paginator ayarları
    paginator = Paginator(blog_list, 5)  # 5 gönderiyi her sayfada göster.
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı göster.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası geçerli aralığın dışındaysa (örn. 9999), son sayfayı göster.
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, 'category_blog.html', context)

def search_view(request):
    query = request.GET.get('q')
    if query:
        all_results = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-date')

        paginator = Paginator(all_results, 5)  # Örnek: 5 sonuç/sayfa
        page = request.GET.get('page')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
    else:
        results = []

    context = {
        'query': query,
        'page_obj': results
    }

    return render(request, 'search_blog.html', context)

