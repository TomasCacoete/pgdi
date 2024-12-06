import funcoes
import statistics
import numpy as np
import analisador

mountain_category = 'Hors Category', 'First Category', 'Second Category', 'Third Category', 'Fourth Category'

#Create KOM's
def start_KOM(activity_points):
    inclinations, _ =  analisador.analizador_atividade(0, len(activity_points), activity_points)
    array_subidas = []
    
    i = 0
    while i < len(inclinations):
        if inclinations[i] > 3:
            begin = activity_points[i]
            start_elevation = begin.elevation
            end_elevation = start_elevation
            difference = 0

            #while i < len(inclinations) and inclinations[i] > 0:
            while i < len(inclinations) and (inclinations[i] > 0 or ( (activity_points[i].elevation - end_elevation) <= - difference * 0.2 and (activity_points[i].elevation - end_elevation) <= -100)):
                i += 1

                if activity_points[i].elevation > end_elevation:
                    end_elevation =  activity_points[i].elevation
                    difference = end_elevation - start_elevation
                

            end = activity_points[i]

            tamanho = funcoes.calculate_distance(begin, end)
            elevacao = funcoes.calculate_difference_of_altitudes(begin, end)
            
            slope = (elevacao / tamanho) * 100

            category = None
            subidas = []

            if elevacao > 800 and slope > 5:
                category = mountain_category[0]
            elif elevacao > 600 and slope > 4:
                category = mountain_category[1]
            elif elevacao > 350 and slope > 3:
                category = mountain_category[2]
            elif elevacao > 200 and slope > 3:
                category = mountain_category[3]
            elif elevacao > 100:
                category = mountain_category[4]

            #Add kom to the array
            if category != None:
                print(f"KOM: {category}, Inicio: {begin}, Fim: {end}, Elevacao: {elevacao}, Slope: {slope}, Tamanho: {tamanho}")
                subidas = [begin, end, category]
                array_subidas.append(subidas)

        i +=1

    return array_subidas
        

#Create Sprint's
def start_sprint(activity_points):
    end_activity = activity_points[-1]
    array_sprint = []

    a = -1
    while funcoes.calculate_distance(activity_points[a], end_activity) < 1000:
        a -= 1

    start_sprint = activity_points[a]
    end_sprint = end_activity
    array_sprint = [start_sprint, end_sprint]
    print(f"Sprint:  Inicio: {start_sprint}, Fim: {end_sprint}")
    return array_sprint

#Create Segments
def create_segments(gpx):
    #GPX File
    activity_gpx_file = gpx

    # Parse the GPX files
    activity_gpx = funcoes.load_route(activity_gpx_file)

    # Get Coordinates from the activity and the predefined route
    activity_points = funcoes.extract_coordinates(activity_gpx)

    sprint = start_sprint(activity_points)
    array_subidas = start_KOM(activity_points)

    return sprint, array_subidas

