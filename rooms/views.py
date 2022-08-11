from cgi import print_exception
from mimetypes import guess_type
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 9
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "pk"


def search(request):
    city = request.GET.get("city", default="Anywhere")
    city = city.capitalize()
    country = request.GET.get("country", default="KR")
    room_type = int(request.GET.get("room_type", default=0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "selected_room_type": room_type,
        "selected_country": country,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
        "selected_amenities": s_amenities,
        "selected_facilities": s_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms}
    )
