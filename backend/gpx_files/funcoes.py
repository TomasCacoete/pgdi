import gpxpy
import geopy.distance




#path of the files
medioFondo_Route = "C:/ProjetoPGDI/pgdi/backend/gpx_files/GFCR-MEDIO-2024.gpx"
grandFondo_coimbra_Route = "C:/ProjetoPGDI/pgdi/backend/gpx_files/GFCR-GRANDE-2024.gpx"
medioFondo_Activity = "C:/ProjetoPGDI/pgdi/backend/gpx_files/Mediofondo.gpx"
treino = "C:/ProjetoPGDI/pgdi/backend/gpx_files/Volta_de_bicicleta_matinal.gpx"
mira = "C:/ProjetoPGDI/pgdi/backend/gpx_files/Coimbra_Tocha_Mira_Coimbra.gpx"
luso = "C:/ProjetoPGDI/pgdi/backend/gpx_files/Luso.gpx"


# Opens and Loads a GPX file
def load_route(filename):
    with open(filename, 'r') as gpx_file:
        return gpxpy.parse(gpx_file)
    
# Extract coordinates from a GPX file    
def extract_coordinates(gpx_file):
    points = []
    for track in gpx_file.tracks:
        for segment in track.segments:
            points.extend(segment.points)
    return points

#Calculate distance between two points
def calculate_distance(point1, point2):
    return geopy.distance.distance(
        (point1.latitude, point1.longitude),
        (point2.latitude, point2.longitude)
    ).meters

#Calculate the inclination as a percentage
def calculate_inclination(point1, point2):
    # Calculate horizontal distance
    distance = calculate_distance(point1, point2)

    # Calculate elevation difference
    elevation_diff = point2.elevation - point1.elevation
    
    # Calculate inclination as a percentage
    if distance > 0:
        inclination_percentage = (elevation_diff / distance) * 100
    else:
        inclination_percentage = 0
    
    return inclination_percentage

#Calculate the speed
def calculate_speed(point1, point2):
    distance = calculate_distance(point1, point2)

    # Calculate speed in km/h
    time_diff = (point2.time - point1.time).total_seconds()
    if time_diff > 0:
        speed = (distance / 1000) / (time_diff / 3600)
    else:
        speed = 0 


    return speed