from django.http import HttpResponse
from django.shortcuts import render
from models import Video


def videos_list(request):
    # videos = Video.objects.all()
    # context = {
    #     'videos': videos,
    #
    return render(request, 'index.html')


def single_video(request, video_slug):
    return HttpResponse("Video:")