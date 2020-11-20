from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import register
from musicbrainzngs import *
import math

# Create your views here.


@register.filter
def get_begin(dictionary):
  return dictionary.get('life-span').get('begin')


@register.filter
def get_release_date(dictionary):
  return dictionary.get('first-release-date')


def index(request):
  query = request.GET.get('searchInput', False)
  if query:
    set_format('json')
    result = search_artists(query, strict=True)
    return render(request, 'musicmeta/index.html', {'artists': result["artists"]})
  else:
    return render(request, 'musicmeta/index.html')


def artist(request, artist_id, page):
  result = browse_release_groups(artist_id, limit=100, offset=page*100)
  print(result)
  count = result['release-group-count']
  pages = math.ceil(count / 100)

  albums, album_compilations, album_lives, singles, single_lives, single_remixes, single_soundtracks, eps, ep_lives, broadcasts, broadcast_lives, others = [
  ], [], [], [], [], [], [], [], [], [], [], []
  for release in result["release-group-list"]:
    if 'secondary-type-list' not in release and release['primary-type'] == 'Album':
      albums.append(release)
    elif 'secondary-type-list' not in release and release['primary-type'] == 'Single':
      singles.append(release)
    elif 'secondary-type-list' not in release and release['primary-type'] == 'EP':
      eps.append(release)
    elif 'secondary-type-list' not in release and release['primary-type'] == 'Broadcast':
      broadcasts.append(release)
    elif release['primary-type'] == 'Album' and release['secondary-type-list'][0] == 'Compilation':
      album_compilations.append(release)
    elif release['primary-type'] == 'Album' and release['secondary-type-list'][0] == 'Live':
      album_lives.append(release)
    elif release['primary-type'] == 'Single' and release['secondary-type-list'][0] == 'Live':
      single_lives.append(release)
    elif release['primary-type'] == 'Single' and release['secondary-type-list'][0] == 'Remix':
      single_remixes.append(release)
    elif release['primary-type'] == 'Single' and release['secondary-type-list'][0] == 'Soundtrack':
      single_soundtracks.append(release)
    elif release['primary-type'] == 'EP' and release['secondary-type-list'][0] == 'Live':
      ep_lives.append(release)
    elif release['primary-type'] == 'Broadcast' and release['secondary-type-list'][0] == 'Live':
      broadcast_lives.append(release)
    else:
      others.append(release)
  albums.sort(key=lambda x: x['first-release-date'])
  album_compilations.sort(key=lambda x: x['first-release-date'])
  album_lives.sort(key=lambda x: x['first-release-date'])
  singles.sort(key=lambda x: x['first-release-date'])
  single_lives.sort(key=lambda x: x['first-release-date'])
  single_remixes.sort(key=lambda x: x['first-release-date'])
  single_soundtracks.sort(key=lambda x: x['first-release-date'])
  eps.sort(key=lambda x: x['first-release-date'])
  ep_lives.sort(key=lambda x: x['first-release-date'])
  broadcasts.sort(key=lambda x: x['first-release-date'])
  broadcast_lives.sort(key=lambda x: x['first-release-date'])
  others.sort(key=lambda x: x['first-release-date'])
  return render(request, 'musicmeta/artist.html', {"pages": range(pages), "page": page, "artist_id": artist_id, "albums": albums, "album_compilations": album_compilations, "album_lives": album_lives, "singles": singles, "single_lives": single_lives, "single_remixes": single_remixes, "single_soundtracks": single_soundtracks, "eps": eps, "ep_lives": ep_lives, "broadcasts": broadcasts, "broadcast_lives": broadcast_lives, "others": others})
  return HttpResponse("You are at artists")
