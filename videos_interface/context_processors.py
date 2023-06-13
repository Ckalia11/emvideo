from .forms import VideoSearchForm

def video_search_form(request):
    form = VideoSearchForm()
    return {'video_search_form': form}