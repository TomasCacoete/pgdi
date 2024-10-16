import gpxpy
import geopy.distance


# Opens and Loads a GPX file
def load_predefined_route(filename):
    with open(filename, 'r') as gpx_file:
        return gpxpy.parse(gpx_file)
    
# Extract coordinates from a GPX file    
def extract_coordinates(gpx_file):
    points = []
    for track in gpx_file.tracks:
        for segment in track.segments:
            points.extend(segment.points)
    return points

# Check if the activity passes through the predefined route
def activity_checker(activity_points,route_points, threshold_distance=50):
    matched_points = 0
    for route_point in route_points:
        for activity_point in activity_points:
            distance = geopy.distance.distance(
                (route_point.latitude, route_point.longitude),
                (activity_point.latitude, activity_point.longitude)
            ).meters
            
            if distance <= threshold_distance:
                matched_points += 1
    return matched_points

# Calculate the matched points percentage and Check if the minimum is met
def check_minimum_matched_points_percentage(matched_points,route_points,minimum_matched_points_percentage = 80 ):
    return (matched_points / len(route_points) * 100) > minimum_matched_points_percentage   

def check_route_passage(activity_gpx_file, predefined_route_file):
    # Parse the GPX files
    activity_gpx = load_predefined_route(activity_gpx_file)
    route_gpx = load_predefined_route(predefined_route_file)
    
    # Get Coordinates from the activity and the predefined route
    activity_points = extract_coordinates(activity_gpx)
    route_points = extract_coordinates(route_gpx)
    
    # Check if the activity passes through the predefined route
    matched_points = activity_checker(activity_points,route_points)

    # Check if the minimum matched points percentage is met and return True or False
    if check_minimum_matched_points_percentage(matched_points,route_points):
        print("The activity passed through the predefined route.")
        return True
    else:
        print("The activity did not pass through the predefined route.")
        return False


