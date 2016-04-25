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

    return render(request, 'news_index.html', context)


def article(request, article_slug):
    current_article = get_object_or_404(Article, pk=article_slug)

    session_vote_state = request.session.get(
        'vote_state_article_%s' % article_slug, 'none')

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
    if request.method == 'POST':
        article_slug = request.POST.get('slug', None)
        current_article = get_object_or_404(Article, slug=article_slug)

        status = request.session['vote_state_article_%s' % article_slug]
        request_type = request.POST.get('type', None)

        if request_type == 'upvote':
            current_article.upvote()
            if status == 'downvoted':
                current_article.cancel_downvote()
            request.session['vote_state_article_%s' % article_slug] = 'upvoted'
        elif request_type == 'cancel_upvote':
            current_article.cancel_upvote()
            request.session['vote_state_article_%s' % article_slug] = 'none'
        elif request_type == 'downvote':
            current_article.downvote()
            if status == 'upvoted':
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