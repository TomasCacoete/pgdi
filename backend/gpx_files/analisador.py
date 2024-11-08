import funcoes


def analizador_atividade(begin, end, activity_points):
    #Arrays to Calculate Average Inclination and Speed
    inclinations = []
    speeds = []

    last_point = activity_points[begin]
    for i in range(begin+1,end):
        inclination = funcoes.calculate_inclination(last_point, activity_points[i])
        speed = funcoes.calculate_speed(last_point, activity_points[i])

        inclinations.append(inclination)
        speeds.append(speed)
                
        last_point = activity_points[i]

    return inclinations, speeds  