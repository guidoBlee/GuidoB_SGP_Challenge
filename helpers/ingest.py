import pandas as pd
import numpy as np
import folium 

import xml.etree.ElementTree as ET


def boat_ingest(team: str ='GBR')->pd.DataFrame:
    """
    Extracts the race start time from an XML file.
    Parameters:
    :param team: The name of the team to be ingested.
    :return: df_boat_dt: A datetime indexed dataframe from the file
    """
    boat_data = pd.read_csv(f"Data/Boat_logs/data_{team.upper()}.csv")
    df_boat = pd.DataFrame(boat_data)

    df_boat["DATETIME"] = pd.to_datetime(df_boat['TIME_LOCAL_unk'])
    df_boat_dt = df_boat.set_index("DATETIME")
    return df_boat_dt

def get_start_time(xml_path: str = "Data/Race_XMLs/25011905_03-13-55.xml") -> pd.Timestamp:
    """
    Extracts the race start time from an XML file.
    Parameters:
    :param xml_path: The file path to the race XML file.
    :return: pd.Timestamp: The race start time as a pandas Timestamp.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    timestr = root.find("RaceStartTime").get("Start")
    return pd.to_datetime(timestr)
   

def ingest_course(xml_path:str ="Data/Race_XMLs/25011905_03-13-55.xml", map_course : bool =True) -> dict:
    # function that ingests an xml, displays a map of the course and returns the gate info
    # gates is a list of dicts, each dict contains the name of the gate and a list of the marks
    # each mark has a lattitude and longitude. 
    # :param xml_path: The file path to the race XML file.
    # :type xml_path: str
    # :param map_course: Whether to display a map of the course (default is True).
    # :type map_course: bool
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract course waypoints (marks)
    allMarks = []
    # gates is a list of all gates, with a sublist of each mark in the compound mark
    gates = []
    course = root.find("Course")
    for compound_mark in course.findall("CompoundMark"):
        gates.append({"name":compound_mark.get("Name"),
                      "marks": []
        })
        for mark in compound_mark.findall("Mark"):
            lat = float(mark.get("TargetLat"))
            lon = float(mark.get("TargetLng"))
            name = mark.get("Name")
            allMarks.append((lat, lon, name))
            gates[-1]["marks"].append({"lat":lat,"lon":lon})
    
    sequence = root.find("CompoundMarkSequence")
    for i, corner in enumerate(sequence.findall("Corner")):
        gates[i]["rounding"] = corner.get("Rounding")
    
    
    limits = []
    # this isn't used for anything except plotting
    for boundary in root.findall("CourseLimit"):
        if boundary.get("avoid") != "0":
            next
        limits.append({"name":boundary.get("name"),
                           "colour":boundary.get("colour"),
                           "lats":[],
                           "lons":[]}
                     )
        for vertex in boundary.findall("Limit"):
            lat = float(vertex.get("Lat"))
            lon = float(vertex.get("Lon"))
            id =  int(vertex.get("SeqID"))
            limits[-1]["lats"].append(lat)
            limits[-1]["lons"].append(lon)
            
    
    if map_course:
        # Create a Folium map centered at the average location
        map_center = [sum([wp[0] for wp in allMarks]) / len(allMarks), sum([wp[1] for wp in allMarks]) / len(allMarks)]
        m = folium.Map(location=map_center, zoom_start=14)
        
        # Add waypoints to the map
        medianPath = []
        for gate in gates:
            gate_lats = [mark["lat"] for mark in gate["marks"]]
            gate_lons = [mark["lon"] for mark in gate["marks"]]
            lat = np.mean(gate_lats)
            lon = np.mean(gate_lons)
            medianPath.append([lat,lon])        
            for lat,lon in zip(gate_lats,gate_lons):
                folium.Marker(location=[lat, lon], icon=folium.Icon(color="blue")).add_to(m)
        
        for limit in limits:
            print([(lon, lat) for lat,lon in zip(limit["lats"],limit["lons"])])
            folium.PolyLine([(lat, lon) for lat,lon in zip(limit["lats"],limit["lons"])], color="black", weight=3).add_to(m)
        
        # Draw course path
        folium.PolyLine([(waypoint[0], waypoint[1]) for waypoint in medianPath], color="blue", weight=3).add_to(m)
        m.show_in_browser()

    print(f"Ingested course with {len(gates)} points.")
    return gates


if __name__ == "__main__":
    print(get_start_time())
    ingest_course()