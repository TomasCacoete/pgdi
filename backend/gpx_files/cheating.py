import analisador
import statistics
import regression

#Check if is cheating by speed and inclination
def check_cheating(begin, end, activity_points):
    
    inclinations, speeds =  analisador.analizador_atividade(begin, end, activity_points)
    cheating = 0
    
    #Checks if the user is cheating by matching with the speed/inclination regression and giving a margin of error - +10%
    for i in range(5,len(speeds)):
        #Calculate the average speed of the last 5 positions
        speed = statistics.mean(speeds[i-5:i])
        #Calculates the average inclination of the last 5 positions
        inclination = statistics.mean(inclinations[i-5:i])
        #Calculate the predicted maximum speed of the last 5 positions
        predicted_maximum_speed = regression.poly(inclination)

        if speed > (predicted_maximum_speed) * 1.10:
            print("YOUR ARE CHEATING!!!\nYou are going at", speed,"km/h in a",inclination,"% zone")
            cheating += 1  

    return inclinations, speeds 

#Calculate the cheating percentage based on the speed and Check if the maximum is surpassed
def check_maximum_cheating_allowed_percentage(cheating,route_points,maximum_cheating_allowed_percentage = 5 ):       
    return (cheating / len(route_points) * 100) <= maximum_cheating_allowed_percentage