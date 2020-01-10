from pprint import pprint

from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.core.paginator import Paginator


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    count = 10
    current_page = int(request.GET.get('page', 1))
    next_page, prev_page = None, None
    info = []
    with open('data-398-2018-08-30.csv', encoding='cp1251') as file:
        reader = csv.DictReader(file)
        for station in reader:
            name = station['Name']
            street = station['Street']
            district = station['District']
            data = {'Name': name, 'Street': street, 'District': district}
            info.append(data)
    paginator_info = Paginator(info, count)
    page_info = paginator_info.get_page(current_page)
    data_name = page_info.object_list
    if page_info.has_previous():
        prev_page = page_info.previous_page_number()
    if page_info.has_next():
        next_page = page_info.next_page_number()
    next_page_url = f'?page={next_page}'
    prev_page_url = f'?page={prev_page}'
    context = {
        'bus_stations': data_name,
        'current_page': page_info.number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
    return render_to_response('index.html', context=context)

