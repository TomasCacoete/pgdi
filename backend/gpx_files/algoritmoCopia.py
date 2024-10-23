import funcoes
import SpeedAnalyser
#import strava2gpx

#Arrays to Calculate Average Inclination and Speed
inclinations = []
speeds = []


activity_gpx_file = funcoes.medioFondo_Activity
predefined_route_file = funcoes.medioFondo_Route

#Check the first point of the route
def check_first_point(point, activity_points, threshold_first_point = 20):
    for i in range(1,len(activity_points)):
        if funcoes.calculate_distance(point, activity_points[i]) <= threshold_first_point:
            print(i)
            return i
    return  False

#Check the last point of the route
def check_last_point(point, activity_points, primeiro_ponto, threshold_first_point = 20):
    for i in range(primeiro_ponto,len(activity_points)):
        if funcoes.calculate_distance(point, activity_points[i]) <= threshold_first_point:
            print(i)
            return i
    return  False

#Check if is cheating by speed and inclination
'''def check_cheating():
    inclination = funcoes.calculate_inclination(last_point, activity_points[k])
    speed = funcoes.calculate_speed(last_point, activity_points[k])

    inclinations.append(inclination)
    speeds.append(speed)

    print(speed)
    print(inclination)
    #Checks if the user is cheating by matching with the speed/inclination regression and giving a margin of error - +10%
    if speed > (SpeedAnalyser.poly(inclination)) * 1.10:
        print("YOUR ARE CHEATING!!!\nYou are going at", speed,"km/h in a",inclination,"% zone")
        cheating += 1
    
    last_point = activity_points[k]'''

    

# Check if the activity passes through the predefined route
def activity_checker(activity_points,route_points, threshold_distance=50):
    #Number of points that match the predeefined route
    matched_points = 0
    cheating = 0

    #Check the first point of the route
    i = check_first_point(route_points[0], activity_points)
    if i and check_last_point(route_points[len(route_points)-1], activity_points, i):

        #First point of the activity, because it is always needed 2 points to calculate speed and inclination
        for j in range(1,len(route_points)-1):
            for k in range(i,i+100):
                distance = funcoes.calculate_distance(route_points[j], activity_points[k])
                #Checks if the distance between the activity and the planned route is smaller than the threshold
                if distance <= threshold_distance:
                    print(k)
                    matched_points += 1
                    i = k
                    break

                if k < len(activity_points)-100:
                    i = k

                
    return matched_points
    #else : return 0

# Calculate the matched points percentage and Check if the minimum is met
def check_minimum_matched_points_percentage(matched_points,route_points,minimum_matched_points_percentage = 95 ):
    a = (matched_points / route_points * 100) 
    print(a)
    return a > minimum_matched_points_percentage

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
    print("Pontos da rota",len(route_points))
    # Check if the minimum matched points percentage is met and return True or False
    if check_minimum_matched_points_percentage(matched_points,len(route_points)):
        print("The activity passed through the predefined route.")
        #If True, the activity is accepted and the summary is showed
        print(matched_points)
        '''print("\nSummary Statistics:")
        print(f"Average inclination: {np.mean(inclinations):.2f}%")
        print(f"Maximum inclination: {max(inclinations):.2f}%")
        print(f"Minimum inclination: {min(inclinations):.2f}%")
        print(f"Average speed: {np.mean(speeds):.2f} km/h")
        print(f"Maximum speed: {max(speeds):.2f} km/h")'''
        return True
    else:
        print("The activity did not pass through the predefined route. ",matched_points)
        return False


check_route_passage(activity_gpx_file, predefined_route_file)