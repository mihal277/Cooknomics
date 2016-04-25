from django.http import HttpResponse
from django.shortcuts import render
from videos.models import Video


def videos_list(request):
    videos = Video.objects.order_by('title')
    context = { 'videos': videos }
    return render(request, 'index.html', context)


def single_video(request, video_slug):
    return HttpResponse("Video:")