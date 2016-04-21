from django.http import HttpResponse


def videos_list(request):
    return HttpResponse("Videos:")


def single_video(request, video_slug):
    return HttpResponse("Video:")