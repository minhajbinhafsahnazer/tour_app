from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Destination, DestinationImage
from .serializers import DestinationSerializer
from tourapp.forms import DestinationForm


# -----------------------
# API VIEWSET
# -----------------------
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    parser_classes = [MultiPartParser, FormParser]

    # ✅ Enable search in API
    filter_backends = [filters.SearchFilter]
    search_fields = ['place_name', 'state', 'district']

    # ✅ Upload image to specific destination
    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        destination = self.get_object()
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({'error': 'No image file provided'}, status=400)

        image = DestinationImage.objects.create(destination=destination, image=image_file)
        return Response({
            'message': 'Image uploaded successfully',
            'image_url': image.image.url
        }, status=201)


# -----------------------
# WEB VIEWS
# -----------------------

# ✅ Home page with search
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


# ✅ Destination detail page
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    images = destination.images.all()  # related_name='images'
    return render(request, 'tourapp/detail.html', {
        'destination': destination,
        'images': images,
    })


# ✅ Create a new destination
def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save()

            # Save single image if provided
            image_file = form.cleaned_data.get('image')
            if image_file:
                DestinationImage.objects.create(destination=destination, image=image_file)

            return redirect('index')
    else:
        form = DestinationForm()

    return render(request, 'tourapp/create_destination.html', {
        'form': form
    })


# ✅ Update destination
def update_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_detail', pk=pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'tourapp/update_destination.html', {
        'form': form,
        'destination': destination
    })


# ✅ Delete destination
def delete_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('index')
    return render(request, 'tourapp/delete_destination.html', {
        'destination': destination
    })


# ✅ About page
def about_view(request):
    return render(request, 'tourapp/about.html')


# ✅ List view for destinations (custom view)
def destination_view(request):
    destinations = Destination.objects.all()
    return render(request, 'tourapp/destination_view.html', {
        'destinations': destinations
    })


# ✅ Static destination carousel (optional)
def static_destinations_list(request):
    destinations = [
        ("India", "A land of diversity, culture, and spirituality."),
        ("UAE", "A modern marvel with architectural wonders."),
        ("China", "An ancient civilization with modern innovation."),
        ("Russia", "Vast landscapes and rich history."),
        ("France", "Romantic vibes and historical treasures."),
        ("Japan", "Where tradition meets technology."),
        ("Egypt", "Pyramids and pharaohs await."),
        ("Brazil", "Vibrant culture and rainforest beauty."),
    ]
    return render(request, 'tourapp/destination_carousel.html', {
        'destinations': destinations
    })
