from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json
from .models import Article


# === Views for news app ===


def news_list(request):
    """

    Generates site containing first page of news list sorted by published_date.
    """
    articles = Article.objects.all().order_by('published_date')

    paginator = Paginator(articles, 20)
    page = paginator.page(1)

    context = {
        'page': page,
    }

    return render(request, 'news_index.html', context)


@require_GET
def news_page(request):
    """
    View to generate updates to news list when user scrolls down the page.

    Returns page_number-th page as JSON.
    """
    page_number = request.GET.get('page', None)

    if page_number is None:
        raise Http404

    articles = Article.objects.all().order_by('published_date')

    paginator = Paginator(articles, 20)

    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    page_data = {'objects': {}}

    for news in page.object_list:
        page_data['objects'][news.slug] = \
            model_to_dict(news, exclude='published_date')
        page_data['objects'][news.slug]['published_date'] = \
            news.published_date.timestamp()
        page_data['objects'][news.slug]['url'] = \
            reverse('news:article', kwargs={'article_slug': news.slug})

    page_data['has_next'] = page.has_next()

    context = {
        "page": page_data
    }

    return HttpResponse(json.dumps(context), content_type='application/json')


def article(request, article_slug):
    """

    Generates site of a given article. Style of elements (i.e. upvote
    and downvote buttons) depends on whether the user already up(down)voted
    the article.

    """
    current_article = get_object_or_404(Article, pk=article_slug)

    session_vote_state = request.session.get(
        'vote_state_article_%s' % article_slug, 'none')

    # check if user already voted
    if session_vote_state == 'upvoted':
        vote_state = 'upvoted'
    elif session_vote_state == 'downvoted':
        vote_state = 'downvoted'
    else:
        vote_state = 'none'

    context = {
        'slug': article_slug,
        'author': current_article.author,
        'title': current_article.title,
        'published_date': current_article.published_date,
        'content': current_article.content,
        'upvotes': current_article.up_votes,
        'downvotes': current_article.down_votes,
        'session_vote_state': vote_state,
    }

    return render(request, 'news_detail.html', context)


@require_POST
def vote(request):
    """

    Generates JSON response to a POST request sent after user up(down)votes
    an article. Part of AJAX interface.
    Requires following parameters to be passed:
    ***slug*** - articles slug
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                cancel_upvote - decrease up_vote count
                downvote - increase down_vote count
                cancel_downvote - decreast down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given article
    ***downvotes*** - down_vote count of given article
    """
    if request.method == 'POST':
        article_slug = request.POST.get('slug', None)
        current_article = get_object_or_404(Article, slug=article_slug)

        status = request.session['vote_state_article_%s' % article_slug]
        request_type = request.POST.get('type', None)

        if request_type == 'upvote':
            current_article.upvote()
            if status == 'downvoted':
                # If the news was already downvoted, downvote count
                # has to be decreased.
                current_article.cancel_downvote()
            request.session['vote_state_article_%s' % article_slug] = 'upvoted'
        elif request_type == 'cancel_upvote':
            current_article.cancel_upvote()
            request.session['vote_state_article_%s' % article_slug] = 'none'
        elif request_type == 'downvote':
            current_article.downvote()
            if status == 'upvoted':
                # If the news was already upvoted, upvote count
                # has to be decreased.
                current_article.cancel_upvote()
            request.session['vote_state_article_%s' % article_slug] = 'downvoted'
        elif request_type == 'cancel_downvote':
            current_article.cancel_downvote()
            request.session['vote_state_article_%s' % article_slug] = 'none'

        context = {
            'upvotes': current_article.up_votes,
            'downvotes': current_article.down_votes,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')
