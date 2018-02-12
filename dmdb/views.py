from django.shortcuts import render
from django.http import HttpResponse
from .models import Dmdb

# Create your views here.
def dmdb_messages(request):
    messages = Dmdb.objects.all()
    xml_data = render(request, 'dmdb_messages.html', {'messages': messages})
    response = HttpResponse(xml_data, content_type='application/xml')
    return response
