import numpy as np


def compass_to_vector(bearing:float) -> np.array:
    # returns a numpy array in cartesian coordinates
    # based on a compass direction. 

    # Remember that the wind is opposite sense!
    v = np.array([np.cos(np.deg2rad(90-bearing)),
                    np.sin(np.deg2rad(90-bearing)),
                    0])
    return v

def vector_to_compass(v:np.array) -> float:
    # v is a vector of latitude, longitude (delta)
    # just need to avoid div0 case. 
    if v[1] == 0:
        if v[0] > 0:
            return 0
        else:
            return 180
    heading = (np.rad2deg(np.atan2(v[1],v[0])) + 360) % 360
    return heading



def coords_to_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the initial bearing (forward azimuth) between two points on Earth.
    :param lat1: Latitude of the initial point in decimal degrees
    :param lon1: Longitude of the initial point in decimal degrees
    :param lat2: Latitude of the destination point in decimal degrees
    :param lon2: Longitude of the destination point in decimal degrees
    :return: Initial bearing in degrees from North
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    
    # Compute differences
    delta_lon = lon2 - lon1
    
    # Compute initial bearing
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
    
    # Compute bearing and convert from radians to degrees
    initial_bearing = np.rad2deg(np.atan2(x, y))
    
    # Normalize bearing to 0-360 degrees
    compass_bearing = (initial_bearing + 360) % 360
    
    return compass_bearing

def coords_to_displacement(lat1, lon1, lat2, lon2,unit=False):
    """
    Calculate the displacement vector (x, y) between two points on Earth.
    :param lat1: Latitude of the initial point in decimal degrees
    :param lon1: Longitude of the initial point in decimal degrees
    :param lat2: Latitude of the destination point in decimal degrees
    :param lon2: Longitude of the destination point in decimal degrees
    :param unit: Whether to return a normalised vector (or not)
    :return: Displacement vector (dx, dy, 0) in meters
    """
    # Radius of the Earth in meters
    R = 6371e3
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    
    # Compute differences
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    # Approximate x and y displacement
    dx = R * delta_lon * np.cos((lat1 + lat2) / 2)
    dy = R * delta_lat

    return_vec = np.array([dx,dy,0])
    # if asked to return a unit vector, do so 
    if unit:
        return_vec = return_vec/np.linalg.norm(return_vec)

    return return_vec

def is_vector_between(A,B,C) -> bool:
    """
    Checks if vector B is 'between' vectors A and C
    using the cross product method.
    
    Parameters:
    A (np.array): First vector
    B (np.array): Vector to (check)
    C (np.array): Second vector
    
    Returns:
    bool: True if v is between a and b, False otherwise
    """
    if False:
        plt.figure(figsize=(5, 5))
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)

        # Plot vectors
        plt.plot([0,A[0]], [0,A[1]], color='r', label='A')
        plt.plot([0,B[0]], [0,B[1]], color='k', label='B')
        plt.plot([0,C[0]], [0,C[1]], color='g', label='C')

        # Set plot limits
        max_val = max(np.linalg.norm(A), np.linalg.norm(B), np.linalg.norm(C)) + 1
        plt.xlim(-max_val, max_val)
        plt.ylim(-max_val, max_val)

        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.show()
    # Compute cross products
    AxB = np.cross(A, B)
    AxC = np.cross(A, C)
    CxB = np.cross(C, B)
    CxA = np.cross(C, A)
    
    # Compute dot products
    condition1 = np.dot(AxB, AxC) >= 0
    condition2 = np.dot(CxB, CxA) >= 0

    # print(f"Condition 1 {condition1}\nCondition2 {condition2}")
    return (condition1 and condition2)



if __name__ == "__main__":
    print(compass_to_vector(0)) # expect 0,1,0
    print(compass_to_vector(45)) # expect # 0.707,0.707, 0
    print(compass_to_vector(90)) # expect # 1,0 ,0
    print(compass_to_vector(270)) # expect #-1, 0, 0 
    
    print(is_vector_between(compass_to_vector(1),
                            compass_to_vector(91),
                            compass_to_vector(184),
                            ))

