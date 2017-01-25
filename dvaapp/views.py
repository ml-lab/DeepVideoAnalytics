from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import requests
import os
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator
from .forms import UploadFileForm
from .models import Video,Frame,Detection
from .tasks import extract_frames

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['name'])
        else:
            raise ValueError
    else:
        form = UploadFileForm()
    context = { 'form' : form }
    context['video_count'] = Video.objects.count()
    context['frame_count'] = Frame.objects.count()
    context['detection_count'] = Detection.objects.count()
    return render(request, 'dashboard.html', context)


def handle_uploaded_file(f,name):
    video = Video()
    video.name = name
    video.save()
    os.mkdir('{}/{}'.format(settings.MEDIA_ROOT,video.pk))
    os.mkdir('{}/{}/video/'.format(settings.MEDIA_ROOT,video.pk))
    os.mkdir('{}/{}/frames/'.format(settings.MEDIA_ROOT,video.pk))
    os.mkdir('{}/{}/indexes/'.format(settings.MEDIA_ROOT, video.pk))
    os.mkdir('{}/{}/detections/'.format(settings.MEDIA_ROOT, video.pk))
    os.mkdir('{}/{}/audio/'.format(settings.MEDIA_ROOT, video.pk))
    primary_key = video.pk
    with open('{}/{}/video/{}.mp4'.format(settings.MEDIA_ROOT,video.pk,video.pk), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    video.uploaded = True
    video.save()
    extract_frames.apply_async(args=[primary_key],queue=settings.Q_EXTRACTOR)

class VideoList(ListView):
    model = Video


class VideoDetail(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        context['frame_list'] = Frame.objects.all().filter(video=self.object)
        context['url'] = '{}/{}/video/{}.mp4'.format(settings.MEDIA_URL,self.object.pk,self.object.pk)
        return context


class FrameList(ListView):
    model = Frame


class FrameDetail(DetailView):
    model = Frame

    def get_context_data(self, **kwargs):
        context = super(FrameDetail, self).get_context_data(**kwargs)
        context['detection_list'] = Detection.objects.all().filter(frame=self.object)
        context['video'] = self.object.video
        context['url'] = '{}/{}/frames/{}.jpg'.format(settings.MEDIA_URL,self.object.video.pk,self.object.time_seconds)
        return context

