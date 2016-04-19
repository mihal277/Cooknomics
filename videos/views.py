from django.http import HttpResponse
from django.shortcuts import render


def videos_list(request):
    return render(request, 'index.html')


def single_video(request, video_slug):
    return HttpResponse("Video:")