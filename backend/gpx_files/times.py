import funcoes
import statistics
import numpy as np
import analisador
import createSegment

def take_time(array_sprint, activity_points, threshold_distance = 50):
    start = array_sprint[0]
    end = array_sprint[1]

    # Find the first point within the threshold distance of the start point
    for a in activity_points:
        distance = funcoes.calculate_distance(start, a)
        if distance <= threshold_distance:
            start = a   
    
    #Split the array activity_points from the start point = a, till the end of the array
    half = [a for a in activity_points if a >= start] 

    # Find the end point within the threshold distance of the end point
    for a in half:
        distance = funcoes.calculate_distance(end, a)
        if distance <= threshold_distance:
            end = a

    # Calculate time in seconds
    time_diff = funcoes.calculate_time(start, end)

    return time_diff


def take_segments_times(gpx, activity_points):
    array_sprint, array_subidas = createSegment.create_segments(gpx)

    sprint_time = take_time(array_sprint, activity_points)
    kom_times = []
    kom_categories = []

    for i in array_subidas:
        kom_times.append(take_time(i, activity_points))
        kom_categories.append(i[2])
    
    return sprint_time, kom_times, kom_categories
