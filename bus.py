from zeep import Client
import json
from lxml import etree as ET
############ Do not change the assignment code value ############
assignment_code = 140110201
name = "Emir"
surname = "Ekici"
student_id = ""
### Do not change the variable names above, just fill them in ###

def announcements(line_code):
    client = Client(wsdl="https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl")
    response = client.service.GetDuyurular_json()
    response_json = json.loads(response)
    announcements = [msg for msg in response_json if msg['HATKODU'] == line_code]
    return len(announcements), [msg['MESAJ'] for msg in announcements]

def stopping_buses():
    client = Client(wsdl="https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl")
    response = client.service.GetFiloAracKonum_json()
    response_json = json.loads(response)
    return [bus['KapiNo'] for bus in response_json]

def max_speeds():
    client = Client(wsdl="https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl")
    response = client.service.GetFiloAracKonum_json()
    response_json = json.loads(response)
    fastest_buses = sorted(response_json, key=lambda x: x['Hiz'], reverse=True)[:3]
    return(fastest_buses)

def show_line_stops(line_code, direction):
    client = Client("https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl")
    response = client.service.DurakDetay_GYY(hat_kodu=line_code)
    response_string = ET.tostring(response)
    return [child[4].text for child in response if child[1].text == direction]

# Function for live tracking of buses and stops
def live_tracking(line_code, direction):
    stops_client = Client(wsdl="https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl")
    stops_response = stops_client.service.DurakDetay_GYY(hat_kodu=line_code)
    stops = [[stop.findtext('DURAKADI'), stop.findtext('YKOORDINATI'), stop.findtext('XKOORDINATI')] for stop in
             stops_response if stop.findtext('YON') == direction]

    buses_client = Client(wsdl="https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl")
    buses_response = buses_client.service.GetHatOtoKonum_json(HatKodu=line_code)
    buses_json = json.loads(buses_response)
    buses = [[bus['kapino'], bus['enlem'], bus['boylam']]
             for bus in buses_json
             if bus['guzergahkodu'].split('_')[1][
                 0] == direction]


    with open('where.js', 'w') as file:
        file.write(f"stops = {stops};\n")
        file.write(f"buses = {buses};\n")

    return stops, buses

print(announcements("E-58"))
print(stopping_buses())
print(max_speeds())
print(show_line_stops("E-58","G"))
print(live_tracking("E-58","G"))
