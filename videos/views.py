from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from videos.models import Video
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
import json

# === Views for video app ===

INITIAL_PAGE_SIZE = 2
NUMBER_OF_ELEMENTS_ON_PAGE = 2


def videos_list(request):
    """

    Generates site containing list of videos sorted by published_date.
    :param request: HttpRequest passed by browser
    :return: HTML rendered from appropriate template with inital data.
    """
    videos = Video.objects.all().order_by('published_date')

    paginator = Paginator(videos, INITIAL_PAGE_SIZE)
    page = paginator.page(1)

    context = {
        'page': page,
        'display_likes': True,
    }

    return render(request, 'video_index.html', context)


@require_GET
def video_page(request):
    """

    View that returns new pages of videos list when user scrolls down the page.
    :param request: HttpRequest passed by broswer, should contain 'page' field
                    that stores number of the page to be fetched from server.
    :return: Requested pages
    """
    page_number = request.GET.get('page', None)

    if page_number is None:
        raise Http404

    # Get sorting parameter, if none is provides, sort by published_date
    sorting = request.GET.get('sorting', 'published_date')

    possible_sortings = ['up_votes', 'published_date', 'title']
    if sorting not in possible_sortings:
        raise Http404

    if sorting == 'up_votes':
        sorting = '-up_votes'

    videos = Video.objects.all().order_by(sorting)
    paginator = Paginator(videos, NUMBER_OF_ELEMENTS_ON_PAGE)

    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    page_data = {'objects': []}

    for video in page.object_list:
        video_dict = model_to_dict(video, exclude=['published_date', 'description'])
        video_dict['slug'] = video.slug
        video_dict['published_date'] = video.published_date.timestamp()
        video_dict['url'] = \
            reverse('videos:single_video', kwargs={'video_slug': video.slug})
        page_data['objects'].append(video_dict)

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
        'slug': video_slug,
        'title': video.title,
        'video_url': video.video_url,
        'published_date': video.published_date,
        'description': video.description,
        'up_votes': video.up_votes,
        'down_votes': video.down_votes,
    }

    return render(request, 'video_detail.html', context)


@require_POST
def vote(request):
    """

    Generates JSON response to a POST request sent after user up(down)votes
    a video. Part of AJAX interface.
    Requires following parameters to be passed:
    ***pk*** - videos database pk
    ***slug*** - videos slug
    ***type*** - type of request, possible choices:
                upvote - increase up_vote count
                downvote - increase down_vote count
    Returns JSON file containing:
    ***upvotes*** - up_vote count of given video
    ***downvotes*** - down_vote count of given video
    ***pk*** - primary key of the up/down voted video
    """
    if request.method == 'POST':
        video_slug = request.POST.get('pk', None)
        current_video = get_object_or_404(Video, pk=video_slug)

        status = request.session.get('vote_state_video_%s' % video_slug, 'none')
        request_type = request.POST.get('type', None)

        # set cookie expiry to 1 year
        request.session.set_expiry(31556926)

        if request_type == 'upvote':
            if status == 'none':
                current_video.upvote()
                request.session['vote_state_video_%s' % video_slug] = 'upvoted'
            elif status == 'upvoted':
                current_video.cancel_upvote()
                request.session['vote_state_video_%s' % video_slug] = 'none'
            elif status == 'downvoted':
                current_video.upvote()
                current_video.cancel_downvote()
                request.session['vote_state_video_%s' % video_slug] = 'upvoted'
        elif request_type == 'downvote':
            if status == 'none':
                current_video.downvote()
                request.session['vote_state_video_%s' % video_slug] = 'downvoted'
            elif status == 'upvoted':
                current_video.cancel_upvote()
                current_video.downvote()
                request.session['vote_state_video_%s' % video_slug] = 'downvoted'
            elif status == 'downvoted':
                current_video.cancel_downvote()
                request.session['vote_state_video_%s' % video_slug] = 'none'

        context = {
            'upvotes': current_video.up_votes,
            'downvotes': current_video.down_votes,
            'pk': current_video.pk,
        }

    return HttpResponse(json.dumps(context), content_type='application/json')
