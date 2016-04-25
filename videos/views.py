from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
from videos.models import Video
from django.views.decorators.http import require_POST
import json


def videos_list(request):
    videos = Video.objects.order_by('title')

    for video in videos:
        video.vote_state = request.session.get(
            'vote_state_video_%s' % video.slug, 'none')

    context = {
        'videos': videos
    }

    return render(request, 'index.html', context)


def single_video(request, video_slug):
    return HttpResponse("Video:")


@require_POST
def vote(request):
    if request.method == 'POST':
        video_slug = request.POST.get('slug', None)
        current_video = get_object_or_404(Video, pk=video_slug)

        status = request.session.get('vote_state_article_%s' % video_slug, 'none')
        request_type = request.POST.get('type', None)

        if request_type == 'upvote':
            current_video.upvote()
            if status == 'downvoted':
                current_video.cancel_downvote()
            request.session['vote_state_article_%s' % video_slug] = 'upvoted'
        elif request_type == 'cancel_upvote':
            current_video.cancel_upvote()
            request.session['vote_state_article_%s' % video_slug] = 'none'
        elif request_type == 'downvote':
            current_video.downvote()
            if status == 'upvoted':
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
