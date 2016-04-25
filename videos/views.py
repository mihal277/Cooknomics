from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from videos.models import Video
from django.views.decorators.http import require_POST
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
    :return: html rendered from apropriate template
    """

    videos = Video.objects.order_by('title')

    for video in videos:
        video.vote_state = request.session.get(
            'vote_state_video_%s' % video.slug, 'none')

    context = {
        'videos': videos
    }

    return render(request, 'index.html', context)


def single_video(request, video_slug):
    """
    TODO
    """
    return HttpResponse("Video:")


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
