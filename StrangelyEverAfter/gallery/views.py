from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from gallery.models import Project, GalleryImage

def index(request):
    latest_project_list = Project.objects.all().order_by('-pub_date')[:5]
    return render_to_response('gallery/index.html', {'latest_project_list': latest_project_list})

def project(request, project_id):
    project_info = get_object_or_404(Project, pk=project_id)
    latest_galleryimage_list = get_list_or_404(GalleryImage, project_id=project_id)
    return render_to_response('gallery/viewproject.html', {
        'project_id': project_id,
        'project_name': project_info.project,
        'latest_galleryimage_list': latest_galleryimage_list
    })

def galleryimage(request, project_id, galleryimage_id):
    project_info = get_object_or_404(Project, pk=project_id)
    image_info = get_object_or_404(GalleryImage, pk=galleryimage_id)
    return render_to_response('gallery/viewimage.html', {
        'project_name': project_info.project,
        'title': image_info.title,
        'location': image_info.location,
        'pub_date': image_info.pub_date
    })
