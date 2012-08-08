from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from gallery.models import Project, Picture
from django.conf import settings

####
import os
import os.path
import re
import Image
from django.template import Library

register = Library()
###


def index(request):
    project_list = Project.objects.all().order_by('-pub_date')[:20]
    return render_to_response('gallery/index.html', {'project_list': project_list})

def project(request, project_id):
    project_info = get_object_or_404(Project, pk=project_id)
    latest_galleryimage_list = get_list_or_404(Picture, project_id=project_id)
    return render_to_response('gallery/viewproject.html', {
        'project_id': project_id,
        'project_name': project_info.project,
        'latest_galleryimage_list': latest_galleryimage_list
    })

def picture(request, project_id, picture_id):
    project_info = get_object_or_404(Project, pk=project_id)
    the_image = Picture.objects.get(pk=picture_id)
    #the_image = '{0}{1}{2}'.format(settings.MEDIA_URL, 'images/', the_image.image)# 'meida/' + the_image.image
    the_image = the_image.thumb.url
    image_info = get_object_or_404(Picture, pk=picture_id)
    return render_to_response('gallery/viewimage.html', {
        'project_name': project_info.project,
        'title': image_info.title,
        'location': the_image,
        'pub_date': image_info.pub_date
    })







































def thumbnail(file, size='100x100x1'):
    # defining the size
    x, y, ratio = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        if ratio == 0:
            image = image.resize([x, y], Image.ANTIALIAS)
        else:
            image.thumbnail([x, y], Image.ANTIALIAS)        
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url


register.filter(thumbnail)