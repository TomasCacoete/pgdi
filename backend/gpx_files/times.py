import funcoes
import statistics
import numpy as np
import analisador
import createSegment

def take_time(array_sprint, activity_points):
    start = array_sprint[0]
    end = array_sprint[1]

    for a in activity_points:
        if a == start:
            start = a
        if a == end:
            end = a

    # Calculate speed in km/h
    time_diff = (end.time - start.time).total_seconds()

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
