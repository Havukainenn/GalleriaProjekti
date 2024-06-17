from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import ImageUploadForm
from .models import Image
from .models import Folder
from django.db import IntegrityError
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def personal_gallery(request):
    user = request.user
    folder_name = request.GET.get('folder')
    search_query = request.GET.get('search', '')  

    images = Image.objects.filter(folder__user=user)
    if folder_name:
        images = images.filter(folder__name=folder_name)
    if search_query:
        images = images.filter(description__icontains=search_query)

    folders = Folder.objects.filter(user=user)
    context = {
        'folders': folders,
        'images': images,
        'search_query': search_query,
        'current_folder': folder_name,
        'search_performed': bool(search_query)  
    }
    return render(request, 'personal_gallery.html', context)

@login_required
def viewImage(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if image.user != request.user:
        return HttpResponseForbidden("You are not authorized to edit or delete this image.")

    if request.method == 'POST':
        if 'delete' in request.POST:
            image.delete()
            return redirect('personal_gallery')
        else:
            form = ImageUploadForm(request.POST, request.FILES, instance=image, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('personal_gallery')
            else:
                return render(request, 'view_image.html', {'image': image, 'form': form})
    else:
        form = ImageUploadForm(instance=image, user=request.user)
        return render(request, 'view_image.html', {'image': image, 'form': form})


@login_required(login_url='login')
def uploadImage(request):
    user = request.user
    folders = user.folder_set.all()  

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        folder_id = request.POST.get('folder')
        folder_new = request.POST.get('folder_new', '').strip()

        if folder_new:
            folder, created = Folder.objects.get_or_create(user=user, name=folder_new)
        elif folder_id and folder_id != 'none':
            folder = Folder.objects.get(id=folder_id, user=user)
        else:
            folder = None

        try:
            for image_file in images:
                Image.objects.create(
                    folder=folder,
                    description=request.POST.get('description', ''),
                    file=image_file,
                    user=user
                )
            return redirect('personal_gallery')
        except IntegrityError as e:
            return render(request, 'upload_image.html', {
                'folders': folders,
                'error': 'There was a problem saving your images. Please try again.',
                'form': ImageUploadForm()  
            })

    return render(request, 'upload_image.html', {'folders': folders})