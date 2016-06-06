from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json
from .models import Article


# === Views for news app ===

INITIAL_PAGE_SIZE = 20
NUMBER_OF_ELEMENTS_ON_PAGE = 20


def news_list(request):
    """

    Generates site containing list of news sorted by published_date.
    :param request: HttpRequest passed by browser
    :return: HTML rendered from appropriate template with inital data.
    """
    articles = Article.objects.all().order_by('published_date')

    paginator = Paginator(articles, INITIAL_PAGE_SIZE)
    page = paginator.page(1)

    context = {
        'page': page,
        'display_likes': True,
    }

    return render(request, 'news_index.html', context)


@require_GET
def news_page(request):
    """

    View that returns new pages of news list when user scrolls down the page.
    :param request: HttpRequest passed by broswer, should contain 'page' field
                    that stores number of the page to be fetched from server.
    :return: Requested pages
    """
    page_number = request.GET.get('page', None)

    if page_number is None:
        raise Http404

    articles = Article.objects.all().order_by('published_date')

    paginator = Paginator(articles, NUMBER_OF_ELEMENTS_ON_PAGE)

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

    Generates site of a given article.

    """
    current_article = get_object_or_404(Article, pk=article_slug)

    context = {
        'slug': article_slug,
        'author': current_article.author,
        'title': current_article.title,
        'published_date': current_article.published_date,
        'content': current_article.content,
        'upvotes': current_article.up_votes,
        'downvotes': current_article.down_votes,
    }

    return render(request, 'news_detail.html', context)


@require_POST
def vote(request):
    """

    Generates JSON response to a POST request sent after user up(down)votes
    a news. Part of AJAX interface.
    Requires following parameters to be passed:
    ***pk*** - news database pk
    ***slug*** - news slug
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                downvote - increase down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given video
    ***downvotes*** - down_vote count of given video
    ***pk*** - primary key of the up/down voted article
    """
    if request.method == 'POST':
        article_slug = request.POST.get('pk', None)
        current_news = get_object_or_404(Article, pk=article_slug)

        status = request.session.get('vote_state_article_%s' % article_slug, 'none')
        request_type = request.POST.get('type', None)

        # set cookie expiry to 1 year
        request.session.set_expiry(31556926)

        if request_type == 'upvote':
            if status == 'none':
                current_news.upvote()
                request.session['vote_state_article_%s' % article_slug] = 'upvoted'
            elif status == 'upvoted':
                current_news.cancel_upvote()
                request.session['vote_state_article_%s' % article_slug] = 'none'
            elif status == 'downvoted':
                current_news.upvote()
                current_news.cancel_downvote()
                request.session['vote_state_article_%s' % article_slug] = 'upvoted'
        elif request_type == 'downvote':
            if status == 'none':
                current_news.downvote()
                request.session['vote_state_article_%s' % article_slug] = 'downvoted'
            elif status == 'upvoted':
                current_news.cancel_upvote()
                current_news.downvote()
                request.session['vote_state_article_%s' % article_slug] = 'downvoted'
            elif status == 'downvoted':
                current_news.cancel_downvote()
                request.session['vote_state_article_%s' % article_slug] = 'none'

        context = {
            'upvotes': current_news.up_votes,
            'downvotes': current_news.down_votes,
            'pk': current_news.pk,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')

