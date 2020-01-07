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
    names = []
    streets = []
    districts = []

    with open('data-398-2018-08-30.csv', encoding='cp1251') as file:
        reader = csv.DictReader(file)
        for station in reader:
            name = station['Name']
            street = station['Street']
            district = station['District']
            names.append(name)
            streets.append(street)
            districts.append(district)
            data = [name, street, district]
            info.append(data)
    paginator_info = Paginator(info, count)
    pag1 = Paginator(names, count)
    pag2 = Paginator(streets, count)
    pag3 = Paginator(districts, count)
    page1 = pag1.get_page(current_page)
    page2 = pag2.get_page(current_page)
    page3 = pag3.get_page(current_page)
    data1 = page1.object_list
    data2 = page2.object_list
    data3 = page3.object_list
    page_info = paginator_info.get_page(current_page)
    data_name = page_info.object_list
    if page_info.has_previous():
        prev_page = page_info.previous_page_number()
    if page_info.has_next():
        next_page = page_info.next_page_number()
    next_page_url = f'?page={next_page}'
    prev_page_url = f'?page={prev_page}'
    masege1 = f'{page_info[0][0]}\n{page_info[1][0]}<br>{page_info[2][0]}<br>{page_info[3][0]}' \
              f'<br>{page_info[4][0]}<br>' \
              f'{page_info[5][0]}<br>{page_info[6][0]}<br>{page_info[7][0]}<br>{page_info[8][0]}' \
              f'<br>{page_info[9][0]}<br>'
    context = {
        'bus_stations': [{'Name': page_info[0][0], 'Street': page_info[1][0], 'District': page_info[2][0]}],
        'current_page': page_info.number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
    return render_to_response('index.html', context=context)

