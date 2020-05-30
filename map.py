import difflib
from difflib  import get_close_matches
import folium
import geocoder
import os
import pandas
import pyowm
import signal
import socket
import sys
import time
from tqdm import tqdm
import webbrowser

width = os.get_terminal_size().columns
dash = '-' * 61
welcome_message = "WEATHER MAP"
exit_message = "THANK YOU"

def error_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" "+'*' * (width-1))
    print(" \n An Unexpected Error Occurred \n\n\t* Check Your Internet Connection.\n\t* Check if the City and Country Match.\n\n\n")
    load_animation(" restarting your console application in ", "987654321", 10, 1, 1)
    welcome_screen()
    
def webpage_open(filename):
    webbrowser.open('file://' + os.path.realpath(filename))
    print(" ")
    print(exit_message.center(width-len(exit_message)))
    print(" "+'*' * (width-1))
    time.sleep(3)
    os.kill(os.getppid(), signal.SIGHUP)
    
def save_map(feature_group, map):
    map.add_child(feature_group)
    filename = "Output-Map.html"
    map.save(filename)
    print("\n Weather Map Generated\n Saved File As : ", filename)
    print(" ")
    webpage_open(filename)

def close_match(wordKey, data):
    if(len(get_close_matches(wordKey, data.Name.values, n = 1, cutoff = 0.6)) == 0 ):
        print("NO")
    closeMatch = get_close_matches(wordKey, data.Name.values, n = 1, cutoff = 0.6)
    print(closeMatch[0])

def user_map():
    try:
        userlocation = geocoder.ip("me")
        map = folium.Map(location = userlocation.latlng, zoom_start = 8)
        feature_group = folium.FeatureGroup(name = "My Map")
        lt = userlocation.latlng[0]
        ln = userlocation.latlng[1]
        la = owm.weather_at_coords(lt,ln)
        w = la.get_weather()
    except TypeError as e:
        error_page()
    message = [str(userlocation.city),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
    feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="red", icon = "glyphicon glyphicon-map-marker")))
    save_map(feature_group, map)
    
def country_map():
    data = pandas.read_csv("country-capitals.csv")
    lat = list(data["CapitalLatitude"])
    lon = list(data["CapitalLongitude"])
    capName = list(data["CapitalName"])
    contName = list(data["ContinentName"])
    map = folium.Map(location = (15,25), zoom_start = 3)
    feature_group = folium.FeatureGroup(name = "My Map")
    print("\n Please Wait \n")
    for lt, ln, nm, cnm in tqdm(zip(lat, lon, capName, contName), total = len(capName), desc = " Progress" ): 
        try:
            if(cnm == 'Antarctica'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="black", icon = "glyphicon glyphicon-map-marker")))
            elif(cnm == 'Asia'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="red", icon = "glyphicon glyphicon-map-marker")))
            elif(cnm == 'Africa'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="darkgreen", icon = "glyphicon glyphicon-map-marker")))
            elif(cnm == 'Australia'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="cadetblue", icon = "glyphicon glyphicon-map-marker")))
            elif(cnm == 'Europe'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="orange", icon = "glyphicon glyphicon-map-marker")))
            elif(cnm == 'North America'):
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="purple", icon = "glyphicon glyphicon-map-marker")))
            else:
                la = owm.weather_at_coords(lt,ln)
                w = la.get_weather()
                message = [str(nm),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="darkred", icon = "glyphicon glyphicon-map-marker")))
        except:
            error_page()      
    save_map(feature_group, map)
    
def desired_map():
    data = pandas.read_csv("country-code.csv")
    country_name = input("\n Enter Country Name : ")
    while(1):
        if(country_name in data.Name.values):
            ccode = list(data.loc[data['Name'] == country_name, 'Code'])[0]
            city_data = pandas.read_csv("world-cities_csv.csv")
            city_name = input("\n Enter City Name : ")
            while(1):
                if((city_name in city_data.name.values)):
                    location = city_name +" "+ ccode
                    print("\n Desired Location : {}\n".format(location))
                    load_animation(" Please Wait...","|/-\\",100,0.075,0)
                    location_coordinates = geocoder.osm(location)
                    sys.stdout.write("\033[F")
                    try:
                        ln = location_coordinates.osm['x']
                        lt = location_coordinates.osm['y']
                    except TypeError as e:
                        error_page()
                    map = folium.Map(location = (lt,ln), zoom_start = 12)
                    feature_group = folium.FeatureGroup(name = "My Map")
                    la = owm.weather_at_coords(lt,ln)
                    w = la.get_weather()
                    message = [location,str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
                    feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="red", icon = "glyphicon glyphicon-map-marker")))
                    save_map(feature_group, map)
                    break
                else:
                    if(len(get_close_matches(city_name, city_data.name.values, n = 5, cutoff = 0.4)) == 0):
                        print("\n NO RESULTS FOUND. TRY AGAIN.\n")
                        city_name = input(" Enter City Name : ")
                    else:
                        city_name = list(get_close_matches(city_name, city_data.name.values, n = 5, cutoff = 0.4))
                        print("\n {0} SIMILAR RESULTS FOUND.\n CHOOSE FROM BELOW.".format(len(city_name)))
                        dash = '-' * 61
                        print(" " + dash)
                        print('{:<52s}{:>6s}'.format(' |  Options'," |  Code |"))
                        print(" " + dash)
                        print('{:<52s}{:>6s}'.format(' | Retry'," |   0   |"))
                        for i in range(len(city_name)):
                            nm = " | "+city_name[i]
                            print('{:<53s}|{:^7d}|'.format(nm,i+1))
                        print(" " + dash)
                        city_response = int(input("\n Enter Response : "))
                        if((city_response-1) != -1) and (city_response <= len(city_name)):
                            city_name = city_name[city_response-1]
                        else:
                            city_name = input(" Enter City Name : ")
            break
        else:
            if(len(get_close_matches(country_name, data.Name.values, n = 1, cutoff = 0.4)) == 0 ):
                print("\n NO RESULTS FOUND. TRY AGAIN.\n")
                country_name = input(" Enter Country Name : ")
            else:
                country_name = list(get_close_matches(country_name, data.Name.values, n = 1, cutoff = 0.4))
                print("\n {0} SIMILAR RESULTS FOUND.\n CHOOSE FROM BELOW.".format(len(country_name)))
                dash = '-' * 61
                print(" " + dash)
                print('{:<52s}{:>6s}'.format(' |  Options'," |  Code |"))
                print(" " + dash)
                print('{:<52s}{:>6s}'.format(' | Retry'," |   0   |"))
                for i in range(len(country_name)):
                    nm = " | "+country_name[i]
                    print('{:<53s}|{:^7d}|'.format(nm,i+1))
                print(" " + dash)
                country_response = int(input("\n Enter Response : "))
                if((country_response -1) != -1) and (country_response <= len(country_name)):
                    country_name = country_name[country_response-1]
                else:
                    country_name = input(" Enter Country Name : ")

def coordinate_map():
    try:
        lt = float(input("\n Enter The Latitude Coordinate : "))
        ln = float(input("\n Enter The Longitude Coordinate : "))
        map = folium.Map(location = (lt,ln), zoom_start = 8)
        feature_group = folium.FeatureGroup(name = "My Map")
        la = owm.weather_at_coords(lt,ln)
        w = la.get_weather()
    except TypeError as e:
        error_page()
    message = [str([lt,ln]),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
    feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="red", icon = "glyphicon glyphicon-map-marker")))
    save_map(feature_group, map)

def welcome_screen():
    check = False
    while(1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" "+'*' * (width-1))
        print(welcome_message.center(width-len(welcome_message)))
        print("\n\n")
        if (check):
            print(" WRONG INPUT. TRY AGAIN.")
        print(" " + dash)
        print('{:<52s}{:>6s}'.format(' |  Options'," |  Code |"))
        print(" " + dash)
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details of Your City","|   1   |"))
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details of National Capitals","|   2   |"))
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details of Desired City","|   3   |"))
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details Based on Coordinates","|   4   |"))
        print('{:<53s}{:>6s}'.format(" |  Exit ","|   5   |"))
        print(" " + dash)
        response = input("\n Enter Your Response : ")
        if(response == '1'):
            user_map()
            break
        elif(response == '2'):
            country_map()
            break
        elif(response == '3'):
            desired_map()
            break
        elif(response == '4'):
            coordinate_map()
            break
        elif(response == '5'):
            print(" ")
            print(exit_message.center(width-len(exit_message)))
            print(" "+'*' * (width-1))
            exit()
        else:
            check = True
        
def load_animation(string_input, animation_input, final_count, speed, controller): 
    load_str = string_input
    animation = animation_input
    anicount = 0
    counttime = 0        
    i = 0                     
    while (counttime != final_count): 
        time.sleep(speed)  
        sys.stdout.write("\r"+ load_str + animation[anicount]+"\t") 
        sys.stdout.flush() 
        anicount = (anicount + 1)% len(animation_input)
        counttime = counttime + 1
    if(controller == 1):
        os.system('cls' if os.name == 'nt' else 'clear')
        
def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    if(is_connected()):
        load_animation("starting your console application...","|/-\\",100,0.075, 1)
        owm = pyowm.OWM('591569bc1f75d583f1852071bad7236d')
        welcome_screen()   
    else:
        print(" \n\n CHECK YOUR INTERNET CONNECTION AND TRY AGAIN...")
        exit(0)
