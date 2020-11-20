from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import register
from musicbrainzngs import *

# Create your views here.


@register.filter
def get_begin(dictionary):
  return dictionary.get('life-span').get('begin')


def index(request):
  query = request.GET.get('searchInput', False)
  if query:
    set_format('json')
    result = search_artists(query)
    print(type(result))
    for artist in result["artists"]:
      print(artist)
  return render(request, 'musicmeta/index.html', {'artists': result["artists"]})
