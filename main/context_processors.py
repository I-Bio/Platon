from .models import *

def global_models(request):
    return { 'subjects_all': Subject.objects.all(), 'units_all': Unit.objects.all() }