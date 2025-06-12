from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from .models import Destination
from .serializers import DestinationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import DestinationImage
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django.shortcuts import render, get_object_or_404, redirect
from tourapp.forms import DestinationForm  # we'll create this soon


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    parser_classes = [MultiPartParser, FormParser]  # for image upload

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        destination = self.get_object()
        image_file = request.FILES.get('image')

        filter_backends = [filters.SearchFilter]  # ✅ Enable search
        search_fields = ['place_name'] 

        if not image_file:
            return Response({'error': 'No image file provided'}, status=400)

        image = DestinationImage.objects.create(destination=destination, image=image_file)
        return Response({
            'message': 'Image uploaded successfully',
            'image_url': image.image.url
        }, status=201)
    

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    images = destination.images.all()  # from related_name='images'
    return render(request, 'tourapp/detail.html', {
        'destination': destination,
        'images': images,
    })
    
def index(request):
    query = request.GET.get('q', '')
    if query:
        destinations = Destination.objects.filter(place_name__icontains=query)
    else:
        destinations = Destination.objects.all()
    return render(request, 'tourapp/index.html', {
        'destinations': destinations,
        'query': query,
    })
    
def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)

        if form.is_valid():
            destination = form.save()

            # Save single image
            image_file = form.cleaned_data.get('image')
            if image_file:
                DestinationImage.objects.create(destination=destination, image=image_file)

            return redirect('index')
    else:
        form = DestinationForm()

    return render(request, 'tourapp/create_destination.html', {
        'form': form
    })



def update_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_detail', pk=pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'tourapp/update_destination.html', {'form': form, 'destination': destination})

def delete_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('index')
    return render(request, 'tourapp/delete_destination.html', {'destination': destination})
