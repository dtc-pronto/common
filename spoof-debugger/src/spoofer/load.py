
from typing import List, Tuple

import xml.etree.ElementTree as ET

def load_kml(path : str) -> List[Tuple[float]]:
    tree = ET.parse(path)
    root = tree.getroot()
    
    # Define the KML namespace
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    coordinates = []

    for point in root.findall('.//kml:Point', namespace):
        coord_element = point.find('kml:coordinates', namespace)
        if coord_element is not None:
            # KML coordinates are in format: longitude,latitude,altitude
            coord_text = coord_element.text.strip()
            if coord_text:
                parts = coord_text.split(',')
                if len(parts) >= 2:
                    longitude = float(parts[0])
                    latitude = float(parts[1])
                    coordinates.append((latitude, longitude))
    
    return coordinates
