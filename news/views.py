from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json
from .models import Article


def news_list(request):
    articles_sorted_by_title = Article.objects.all().order_by('title')
    articles_sorted_by_date = Article.objects.all().order_by('published_date')

    context = {
        'by_title': articles_sorted_by_title,
        'by_date': articles_sorted_by_date,
    }

    return render(request, 'news/news_list.html', context)


def article(request, article_slug):
    article = get_object_or_404(Article, pk=article_slug)

    session_vote_state = request.session.get('vote_state_%s' %article_slug, 'none')

    if session_vote_state == 'upvoted':
        vote_state = 'upvoted'
    elif session_vote_state == 'downvoted':
        vote_state = 'downvoted'
    else:
        vote_state = 'none'

    context = {
        'slug': article_slug,
        'author': article.author,
        'title': article.title,
        'published_date': article.published_date,
        'content': article.content,
        'upvotes': article.up_votes,
        'downvotes': article.down_votes,
        'session_vote_state': vote_state,
    }

    return render(request, 'news/article.html', context)

@require_POST
def vote(request):
    if request.method == 'POST':
        article_slug = request.POST.get('slug', None)
        article = get_object_or_404(Article, slug=article_slug)

        status = request.session['vote_state_%s' %article_slug]

        request_type = request.POST.get('type', None)
        print('REQUEST TYPE = %s' %request_type)

        if request_type == 'upvote':
            article.upvote()
            if status == 'downvoted':
                article.cancel_downvote()

            request.session['vote_state_%s' %article_slug] = 'upvoted'
        elif request_type == 'cancel_upvote':
            article.cancel_upvote()
            request.session['vote_state_%s' %article_slug] = 'none'
        elif request_type == 'downvote':
            article.downvote()
            if status == 'upvoted':
                article.cancel_upvote()

            request.session['vote_state_%s' %article_slug] = 'downvoted'
        elif request_type == 'cancel_downvote':
            article.cancel_downvote()
            request.session['vote_state_%s' %article_slug] = 'none'

        context = {
            'upvotes': article.up_votes,
            'downvotes': article.down_votes,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')