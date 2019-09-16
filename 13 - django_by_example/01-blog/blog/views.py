from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
# Create your views here.


def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


class PostListVieww(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 显示相近 Tag 的文章列表
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form,
                      'similar_posts': similar_posts
                  })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_FROM, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.changed_data['query']
            # results = Post.objects.annotate(search=SearchVector('title', 'slug', 'body'),).filter(search=query)

            # search_vector = SearchVector('title', 'body')
            # search_query = SearchQuery(query)
            # results = Post.objects.annotate(search=search_vector, rank=SearchRank(
            #     search_vector, search_query)).filter(search=search_query).order_by('-rank')

            search_query = SearchQuery(query)
            search_vector = SearchVector(
                'title', weight='A') + SearchVector('body', weight='B')
            # results = Post.objects.annotate(search=search_vector, rank=SearchRank(
            #     search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')

            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gte=0.1).order_by('-similarity')

    return render(request, 'blog/post/search.html', {'query': query, 'form': form, 'results': results})
