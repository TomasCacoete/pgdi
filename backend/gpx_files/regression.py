import funcoes
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

inclinations = []
speeds = []

speed_regression = []
inclination_regression = []

def atividade(activity_points):
    last_point = activity_points[0]
    for i in range(1, len(activity_points)):
        activity_point = activity_points[i]
        inclination = funcoes.calculate_inclination(last_point,activity_point)
        speed = funcoes.calculate_speed(last_point,activity_point)
                
        inclinations.append(inclination)
        speeds.append(speed)

        if i>5 :
            speed  = 0
            inclination = 0
            for j in range(i-5,i):
                speed += speeds[j]/5
                inclination += inclinations[j]/5
            speed_regression.append(speed*1.6+abs(inclination*5))
            inclination_regression.append(inclination)

        last_point = activity_point


def create_regression(activity_points1, activity_points2):
    
            
    atividade(activity_points1)
    atividade(activity_points2)
    
    # Perform quadratic regression
    coefficients = np.polyfit(inclination_regression, speed_regression,1)

    # Create a polynomial function from the coefficients
    poly = np.poly1d(coefficients)
    print(poly)
    return speed_regression, inclination_regression, coefficients, poly


treino = funcoes.load_route(funcoes.luso)
treino = funcoes.extract_coordinates(treino)
treino2 = funcoes.load_route(funcoes.mira)
treino2 = funcoes.extract_coordinates(treino2)
speed_regression, inclination_regression, coefficients, poly = create_regression(treino, treino2)


# Generate points for plotting
x_line = np.linspace(min(inclination_regression), max(inclination_regression), 100)
y_line = poly(x_line)


# Create the plot
'''
plt.figure(figsize=(10, 6))
plt.scatter(inclination_regression, speed_regression, alpha=0.5)
plt.plot(x_line, y_line, color='red')
plt.xlabel('Inclination (%)')
plt.ylabel('Speed (km/h)')
plt.title('Speed vs Inclination (Quadratic Regression)')
plt.grid(True)


#plt.show()
'''

'''
print("\nRegression Analysis:")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")


# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(inclinations, speeds, alpha=0.5)
plt.plot(inclinations, slope * np.array(inclinations) + intercept, color='red')
plt.xlabel('Inclination (%)')
plt.ylabel('Speed (km/h)')
plt.title('Speed vs Inclination')
plt.grid(True)
plt.show()'''

