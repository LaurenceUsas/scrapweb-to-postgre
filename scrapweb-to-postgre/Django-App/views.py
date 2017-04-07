import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import RawData, UnitInformation, UnitHistory
import json

def index(request):
    return HttpResponse("Index page")

@csrf_exempt
def upload(request):

    def upload_to_history(apt):
        apt_h = UnitHistory()
        apt_h.apartment = apt
        apt_h.price = apt.price
        apt_h.status = apt.status
        apt_h.save()
        print("Apartment %s added to UnitHistory database" %apt.construction_ref)

    def assign_scrapped_data(item):
        apartment = UnitInformation()
        apartment.construction_ref = item['C_Ref']
        apartment.number = item['AptNo']
        apartment.bedrooms = item['Beds']
        apartment.floor = item['Lvl']
        apartment.area = item['AreaSqM']
        apartment.price = item['Price']
        apartment.status = item['Status']

        return apartment

    # Receives JSON of apartments
    json_string = str(request.body, encoding='utf-8')
    new_data_json = json.loads(json_string)

    # Upload data to RawData table 
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    if RawData.objects.filter(date=date):
        print("Error! There is entry with todays date already!")
    else:
        raw = RawData(raw_data=new_data_json)
        raw.save()

    # Get and map data for comparison
    old_data = UnitInformation.objects.all()
    new_data = []
    for new_apt in new_data_json['Apartments']:
        new_data.append(assign_scrapped_data(new_apt))

    # find changes and upload
    for new in new_data:
        unit_data = UnitInformation.objects.filter(construction_ref=new.construction_ref)
        if unit_data.count() != 0:
            old = unit_data[0]
            # print("Unit %s exists!" %new.name)
            if new.status != old.status:
                print("..and status changed.")
                upload_to_history(old)
            elif new.price != old.price:
                print("..and price changed.")
                upload_to_history(new)
        else:
            if new.status != 'Available':
                new.save()
                upload_to_history(new)

    # Update data to UnitInformation table
    for new_apt in new_data:
        new_apt.save()

    return HttpResponse(json_string)
