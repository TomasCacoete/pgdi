import funcoes
import SpeedAnalyser
import numpy as np
#import strava2gpx

#Arrays to Calculate Average Inclination and Speed
inclinations = []
speeds = []




activity_gpx_file = funcoes.treino
predefined_route_file = funcoes.grandFondo_coimbra_Route


# Check if the activity passes through the predefined route
def activity_checker(activity_points,route_points, threshold_distance=50):
    #Number of points that match the predeefined route
    matched_points = 0
    cheating = 0
    #First point of the activity, because it is always needed 2 points to calculate speed and inclination
    last_point = activity_points[0]
    for route_point in route_points:
        for activity_point in activity_points[1:]:
            distance = funcoes.calculate_distance(route_point, activity_point)
            #Checks if the distance between the activity and the planned route is smaller than the threshold
            if distance <= threshold_distance:
                matched_points += 1


            inclination = funcoes.calculate_inclination(last_point,activity_point)
            speed = funcoes.calculate_speed(last_point,activity_point)
            
            #Checks if the user is cheating by matching with the speed/inclination regression and giving a margin of error - +10%
            if speed > (SpeedAnalyser.intercept + inclination * SpeedAnalyser.slope) * 1.10:
                print("YOUR ARE CHEATING!!!\nYou are going at", speed,"km/h in a",inclination,"% zone")
                cheating += 1

            inclinations.append(inclination)
            speeds.append(speed)

            last_point = activity_point
    return matched_points

# Calculate the matched points percentage and Check if the minimum is met
def check_minimum_matched_points_percentage(matched_points,route_points,minimum_matched_points_percentage = 80 ):
    return (matched_points / len(route_points) * 100) > minimum_matched_points_percentage

#Calculate the cheating percentage based on the speed and Check if the maximum is surpassed
def check_maximum_cheating_allowed_percentage(cheating,route_points,maximum_cheating_allowed_percentage = 5 ):       
    return (cheating / len(route_points) * 100) <= maximum_cheating_allowed_percentage

def check_route_passage(activity_gpx_file, predefined_route_file):
    # Parse the GPX files
    activity_gpx = funcoes.load_route(activity_gpx_file)
    route_gpx = funcoes.load_route(predefined_route_file)
    
    # Get Coordinates from the activity and the predefined route
    activity_points = funcoes.extract_coordinates(activity_gpx)
    route_points = funcoes.extract_coordinates(route_gpx)
    
    # Check if the activity passes through the predefined route
    matched_points = activity_checker(activity_points,route_points)

    # Check if the minimum matched points percentage is met and return True or False
    if check_minimum_matched_points_percentage(matched_points,route_points) and check_maximum_cheating_allowed_percentage:
        print("The activity passed through the predefined route.")
        #If True, the activity is accepted and the summary is showed
        print("\nSummary Statistics:")
        print(f"Average inclination: {np.mean(inclinations):.2f}%")
        print(f"Maximum inclination: {max(inclinations):.2f}%")
        print(f"Minimum inclination: {min(inclinations):.2f}%")
        print(f"Average speed: {np.mean(speeds):.2f} km/h")
        print(f"Maximum speed: {max(speeds):.2f} km/h")
        return True
    else:
        print("The activity did not pass through the predefined route.")
        return False


check_route_passage(activity_gpx_file, predefined_route_file)