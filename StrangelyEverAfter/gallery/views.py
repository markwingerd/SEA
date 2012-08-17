from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from gallery.models import Project, Picture
from django.conf import settings

import os
import os.path
import re
import Image
from django.template import Library

register = Library()

def index(request):
    project_list = Project.objects.all().order_by('-pub_date')[:20]
    return render_to_response('gallery/index.html', {'project_list': project_list})

def project(request, project_id):
    project_info = get_object_or_404(Project, pk=project_id)
    galleryimage_list = get_list_or_404(Picture, project_id=project_id)

    # Create a list of 5 item lists of pictures
    image_list = ()
    inner_list = ()
    for i in range(0, len(galleryimage_list), 5):
        for img in galleryimage_list[i:i+5]:
            inner_list += (img,)
        image_list += (inner_list,)
        inner_list = ()
    return render_to_response('gallery/viewproject.html', {
        'project_name': project_info.project,
        'banner_image': project_info.banner.url,
        'galleryimage_list': galleryimage_list
    })



def picture(request, project_id, picture_id):
    project_info = get_object_or_404(Project, pk=project_id)
    the_image = Picture.objects.get(pk=picture_id)
    the_image = the_image.image.url
    image_info = get_object_or_404(Picture, pk=picture_id)
    return render_to_response('gallery/viewimage.html', {
        'project_name': project_info.project,
        'title': image_info.title,
        'location': the_image,
        'pub_date': image_info.pub_date
    })