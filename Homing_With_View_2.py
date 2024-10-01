#Check notes Below
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
from datetime import datetime

def check_if_hit(missile, target, threshold=0.1):
    distance = ((missile[0] - target[0])**2 + 
                (missile[1] - target[1])**2 + 
                (missile[2] - target[2])**2)**0.5
    print("Distance to Hit Target: ", distance)
    return distance <= threshold


def update_missile_loc(missile, target, speed, time_per_move):
    missile_direction_vector = []
    magnitude = 0
    for i in range(3):
        missile_direction_vector.append(target[i] - missile[i])
        magnitude += missile_direction_vector[i]**2
    magnitude = magnitude**0.5
    
    if magnitude > 0:  
        missile_direction_vector = [d / magnitude for d in missile_direction_vector]

    move_distance = speed * time_per_move

    if move_distance >= magnitude:
        missile[:] = target[:]
    else:
        for i in range(3):
            missile[i] += missile_direction_vector[i] * move_distance

def update_interceptor_loc(intercept, missile, intercept_speed, time_per_move):
    interceptor_direction_vector = []
    magnitude = 0
    for i in range(3):
        interceptor_direction_vector.append(missile[i] - intercept[i])
        magnitude += interceptor_direction_vector[i]**2
    magnitude = magnitude**0.5
    
    if magnitude > 0:
        interceptor_direction_vector = [d / magnitude for d in interceptor_direction_vector]

    move_distance = intercept_speed * time_per_move

    if move_distance >= magnitude:
        intercept[:] = missile[:]
    else:
        for i in range(3):
            intercept[i] += interceptor_direction_vector[i] * move_distance

def check_if_intercepted(intercept, missile, threshold=0.1):
    distance = ((missile[0] - intercept[0])**2 + 
                (missile[1] - intercept[1])**2 + 
                (missile[2] - intercept[2])**2)**0.5
    print("Distance to Hit Missile: ", distance)
    return distance <= threshold

#Note: Space dimensions in km
missile = [0.0, 4000.0, 8000.0]
intercept = [6000.0, 10000.0, 0.0]
target_hit = [8000.0, 6000.0, 0.0]

#Note: Speed in m/s
missile_speed = 800
intercept_speed = 650
time_per_move = 0.2
intercepted = False

#Note: The Dimensions Could be Changed to Be Bigger or Smaller Before Running the Program. Nothing is Static.
#Note: The Speeds Could be Changed to Be Faster or Slower Before Running the Program. Nothing is Static.

missile_positions = []
interceptor_positions = []


while not intercepted:
    print("Missile Coordinates: ", missile, "\nInterceptor Coordinates: ", intercept, "\nTarget Coordinates: ", target_hit)
    missile_positions.append(missile.copy())
    interceptor_positions.append(intercept.copy())
    
    update_missile_loc(missile, target_hit, missile_speed, time_per_move)
    update_interceptor_loc(intercept, missile, intercept_speed, time_per_move)
    hit = check_if_hit(missile, target_hit)
    intercepted = check_if_intercepted(intercept, missile)
    
    print("Time : ", datetime.now().strftime("%H:%M:%S.%f")[:-3], "\n")
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 10000)
    ax.set_ylim(0, 10000)
    ax.set_zlim(0, 10000)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    t_missile_positions = np.array(missile_positions)
    t_interceptor_positions = np.array(interceptor_positions)

    ax.plot(t_missile_positions[:, 0], t_missile_positions[:, 1], t_missile_positions[:, 2], label='Missile Path', color='r', marker='.')
    ax.plot(t_interceptor_positions[:, 0], t_interceptor_positions[:, 1], t_interceptor_positions[:, 2], label='Interceptor Path', color='b', marker='.')
    ax.scatter(target_hit[0], target_hit[1], target_hit[2], label='Target Position', color='g', s=100)
    
    ax.legend()
    plt.show()
    
    
    if intercepted:
        print("\nInterception Successful.")
        break
    if hit:
        print("\nInterception Failed.")
        break
    time.sleep(time_per_move)
