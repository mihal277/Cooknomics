from django.http import HttpResponse


def videos_list(request):
    return HttpResponse("Videos:")


def single_video(request, vid_id):
    return HttpResponse("Video:")