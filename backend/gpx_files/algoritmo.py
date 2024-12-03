import funcoes
import statistics
import numpy as np
import cheating
import times


activity_gpx_file = funcoes.subida
predefined_route_file = funcoes.subida

#Check the first point of the route
def check_first_point(point, activity_points, threshold_first_point = 20):
    for i in range(1,len(activity_points)):
        if funcoes.calculate_distance(point, activity_points[i]) <= threshold_first_point:
            return i
    return  False

#Check the last point of the route
def check_last_point(point, activity_points, primeiro_ponto, threshold_first_point = 20):
    for i in range(len(activity_points)-1,primeiro_ponto, -1):
        if funcoes.calculate_distance(point, activity_points[i]) <= threshold_first_point:
            return i
    return  False


# Check if the activity passes through the predefined route
def activity_checker(activity_points,route_points, threshold_distance=50):
    #Number of points that match the predeefined route
    matched_points = 0
    index_points = []
    #Value to return
    begin_return = check_first_point(route_points[0], activity_points)

    #Check the first and last point of the route
    begin = check_first_point(route_points[0], activity_points)
    end = check_last_point(route_points[-1], activity_points, begin)
    if begin and end:

        #First point of the activity, because it is always needed 2 points to calculate speed and inclination
        for j in range(1,len(route_points)-1):
            for k in range(begin,begin+100):
                distance = funcoes.calculate_distance(route_points[j], activity_points[k])
                #Checks if the distance between the activity and the planned route is smaller than the threshold
                if distance <= threshold_distance:
                    matched_points += 1
                    if k < len(activity_points)-100:
                        begin = k
                    index_points.append(k)
                    break

    return matched_points, begin_return, end 

# Calculate the matched points percentage and Check if the minimum is met
def check_minimum_matched_points_percentage(matched_points,route_points,minimum_matched_points_percentage = 95 ):
    a = (matched_points / route_points * 100) 
    return a > minimum_matched_points_percentage


def check_route_passage(activity_gpx_file, predefined_route_file):
    #Arrays to Calculate Average Inclination and Speed
    inclinations = []
    speeds = []

    # Parse the GPX files
    activity_gpx = funcoes.load_route(activity_gpx_file)
    route_gpx = funcoes.load_route(predefined_route_file)
    
    # Get Coordinates from the activity and the predefined route
    activity_points = funcoes.extract_coordinates(activity_gpx)
    route_points = funcoes.extract_coordinates(route_gpx)

    # Check if the activity passes through the predefined route
    matched_points, begin, end = activity_checker(activity_points,route_points)
    print("Pontos da rota",len(route_points))
    print(begin, end)

    # Check if the maximum cheating allowed percentage is surpassed and return True or False
    inclinations, speeds = cheating.check_cheating(begin, end, activity_points)

    # Check if the minimum matched points percentage is met and return True or False
    if check_minimum_matched_points_percentage(matched_points,len(route_points)):
        print("The activity passed through the predefined route.")
        #If True, the activity is accepted and the summary is showed
        print(matched_points)
        print("\nSummary Statistics:")
        print(f"Average inclination: {statistics.mean(inclinations[:]):.2f}%")
        print(f"Maximum inclination: {max(inclinations[:]):.2f}%")
        print(f"Minimum inclination: {min(inclinations[:]):.2f}%")
        print(f"Average speed: {statistics.mean(speeds[:]):.2f} km/h")
        print(f"Maximum speed: {max(speeds[:]):.2f} km/h")

        sprint_time, kom_times = times.take_segments_times(funcoes.subida, activity_points)
        print(sprint_time, kom_times)

        total_time = funcoes.calculate_time(activity_points[0], activity_points[-1])
        print(total_time)
        return total_time
    else:
        print("The activity did not pass through the predefined route. ",matched_points)
        total_time = None
        return total_time


check_route_passage(activity_gpx_file, predefined_route_file)