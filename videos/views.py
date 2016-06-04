from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from videos.models import Video
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json

# === Views for video app ===


def videos_list(request):
    """

    Generates site containing list of videos sorted by title.
    Adds a ***vote_state*** field to every video object passed
    to template that contains information about whether user already
    upvoted or downvoted the video. Style of like button objects
    depend on this parameter.

    :param request: HttpRequest passed by browser
    :return: html rendered from appropriate template
    """
    videos = Video.objects.all().order_by('published_date')

    paginator = Paginator(videos, 1)
    page = paginator.page(1)

    context = {
        'page': page,
    }

    return render(request, 'video_index.html', context)


@require_GET
def video_page(request):
    """
    View to generate updates to videos list when user scrolls down the page.

    Returns page_number-th page as JSON.
    """
    page_number = request.GET.get('page', None)

    if page_number is None:
        raise Http404

    videos = Video.objects.all().order_by('published_date')
    paginator = Paginator(videos, 1)

    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    page_data = {'objects': {}}

    for video in page.object_list:
        page_data['objects'][video.slug] = \
            model_to_dict(video, exclude='published_date')
        page_data['objects'][video.slug]['published_date'] = \
            video.published_date.timestamp()
        page_data['objects'][video.slug]['url'] = \
            reverse('videos:single_video', kwargs={'video_slug': video.slug})

    page_data['has_next'] = page.has_next()

    context = {
        "page": page_data
    }

    return HttpResponse(json.dumps(context), content_type='application/json')


def single_video(request, video_slug):
    """
    TODO
    """
    video = get_object_or_404(Video, pk=video_slug)

    context = {
        'video': video
    }

    return render(request, 'video_detail.html', context)


@require_POST
def vote(request):
    """

    Generates JSON response to a POST request sent after user up(down)votes
    a video. Part of AJAX interface.
    Requires following parameters to be passed:
    ***slug*** - videos slug
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                cancel_upvote - decrease up_vote count
                downvote - increase down_vote count
                cancel_downvote - decreast down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given video
    ***downvotes*** - down_vote count of given video
    """
    if request.method == 'POST':
        video_slug = request.POST.get('slug', None)
        current_video = get_object_or_404(Video, pk=video_slug)

        status = request.session.get('vote_state_article_%s' % video_slug, 'none')
        request_type = request.POST.get('type', None)

        if request_type == 'upvote':
            current_video.upvote()
            if status == 'downvoted':
                # If the video was already downvoted, downvote count
                # has to be decreased.
                current_video.cancel_downvote()
            request.session['vote_state_article_%s' % video_slug] = 'upvoted'
        elif request_type == 'cancel_upvote':
            current_video.cancel_upvote()
            request.session['vote_state_article_%s' % video_slug] = 'none'
        elif request_type == 'downvote':
            current_video.downvote()
            if status == 'upvoted':
                # If the news was already upvoted, upvote count
                # has to be decreased.
                current_video.cancel_upvote()
            request.session['vote_state_article_%s' % video_slug] = 'downvoted'
        elif request_type == 'cancel_downvote':
            current_video.cancel_downvote()
            request.session['vote_state_article_%s' % video_slug] = 'none'

        context = {
            'upvotes': current_video.up_votes,
            'downvotes': current_video.down_votes,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
####### WIDOKI DO WYSZUKIWANIA DLA MAJKELA ###########

# widok ktory zwraca AJAXEM liste produktow
@require_GET
def get_items(request):
    items = Video.objects.all().order_by('title')

    # te video wzialem jako przyklad, powinny byc elementy nazwa: primary_key
    context = []
    for item in items:
        context.append({item.title: item.pk})

    return HttpResponse(json.dumps(context), content_type='application/json')

@require_GET
def process_items(request):
    # sprawdz czy dane nie sa puste
    if not request.GET:
        return HttpResponse(status=400)

    # kazdy element to primary_key elementu
    for element in request.GET:
        print(element)

    return HttpResponse(json.dumps({}), content_type="application/json")
