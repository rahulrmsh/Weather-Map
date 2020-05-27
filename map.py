import folium
import pandas
import geocoder
import pyowm
import os
from tqdm import tqdm
import webbrowser
import time
import sys

def webpage_open(filename):
    webbrowser.open('file://' + os.path.realpath(filename))
    exit()
    
def save_map(feature_group, map):
    map.add_child(feature_group)
    filename = "Weather-Map.html"
    map.save(filename)
    print(" Weather Map Generated\n Saved File As : ", filename)
    print(" ")
    webpage_open(filename)

def country_map():
    animation = "|/-\\"
    data = pandas.read_csv("country-capitals.csv")
    lat = list(data["CapitalLatitude"])
    lon = list(data["CapitalLongitude"])
    capName = list(data["CapitalName"])
    contName = list(data["ContinentName"])
    map = folium.Map(location = (15,25), zoom_start = 3)
    feature_group = folium.FeatureGroup(name = "My Map")
    print("\n Please Wait \n")
    for lt, ln, nm, cnm in tqdm(zip(lat, lon, capName, contName), total = len(capName), desc = " Progress" ): 
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
    save_map(feature_group, map)
    
def user_map():
    map = folium.Map(location = userlocation.latlng, zoom_start = 8)
    feature_group = folium.FeatureGroup(name = "My Map")
    lt = userlocation.latlng[0]
    ln = userlocation.latlng[1]
    la = owm.weather_at_coords(lt,ln)
    w = la.get_weather()
    message = [str(userlocation.city),str(w.get_status()),str(w.get_temperature(unit='celsius')['temp'])+"&#176; C"]
    feature_group.add_child(folium.Marker(location=[float(lt), float(ln)], popup = ",\n".join(message), icon = folium.Icon(color="red", icon = "glyphicon glyphicon-map-marker")))
    save_map(feature_group, map)
    
def welcome_screen():
    while(1):
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        welcome_message = "WORLD MAP"
        print(" "+'*' * (width-1))
        print(welcome_message.center(width-len(welcome_message)))
        print("\n\n")
        dash = '-' * 61
        print(" " + dash)
        print('{:<52s}{:>6s}'.format(' |  Options'," |  Code |"))
        print(" " + dash)
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details of Your City","|   1   |"))
        print('{:<53s}{:>6s}'.format(" |  Print Weather Details of National Capitals","|   2   |"))
        print(" " + dash)
        response = input("\n Enter Your Response : ")
        if(response == '1'):
            user_map()
            break
        elif(response == '2'):
            country_map()
            break
        
def load_animation(): 
    os.system('cls' if os.name == 'nt' else 'clear')
    load_str = "starting your console application..."
    animation = "|/-\\"
    anicount = 0
    counttime = 0        
    i = 0                     
    while (counttime != 100): 
        time.sleep(0.075)  
        sys.stdout.write("\r"+ load_str + animation[anicount]) 
        sys.stdout.flush() 
        anicount = (anicount + 1)% 4
        counttime = counttime + 1
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    load_animation()
    owm = pyowm.OWM('591569bc1f75d583f1852071bad7236d') 
    userlocation = geocoder.ip("me")
    welcome_screen()   
