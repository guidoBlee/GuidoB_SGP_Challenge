import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import folium

import seaborn as sns
import numpy as np
from . import maths


def reflect_heading(hdg,TWD):
    """
    Reflect a compass direction about another (usually the TWD)
    :param hdg: compass direction to reflect
    :param TWD: direction about which to reflect
    :return: New direction reflected about TWD parameter
    """
    new_headng =(TWD - (hdg-TWD) + 720) % 360
    return new_headng


def manv_required(twa_min=45,twa_max=135,starboard=False,dest_bearing=270,TWD=0):
    """
    Calculates if the desired bearing is between the currently accessible 
    :param twa_min: Highest upwind mode reachable
    :param twa_max: Lowest downwind mode reachable
    :param starboard: Boolean value whether vessel is on starboard relative to wind
    :param TWD: True Wind Direction
    :return: Boolean True if manoeuvre required.
    """
    
    # changed twa_min and twa_max depending on tack
    if starboard:
         twa_min = reflect_heading(twa_min,TWD)
         twa_max = reflect_heading(twa_max,TWD)
    
    # print(f"Checking - {twa_min}S {dest_bearing} {twa_max}")
    # change into vectors
    twa_min_vector = maths.compass_to_vector(twa_min)
    twa_max_vector = maths.compass_to_vector(twa_max)
    bearing_vector = maths.compass_to_vector(dest_bearing)
   
   # if the desired bearing is between the two, no manoeuvre is required. 
   # otherwise, yes
    if maths.is_vector_between(twa_min_vector,bearing_vector,twa_max_vector):
        return False
    return True



if __name__ == "__main__":
    # Example Usage:
    a = np.array([0,1])   # Vector a
    b = np.array([1,0])   # Vector b
    v1 = np.array([0.5, 0.5])  # Vector v (inside the range)
    v2 = np.array([-1, -1])    # Vector v (outside the range)

    print(maths.is_vector_between(a, v1, b))  # Expected: True
    print(maths.is_vector_between(a, v2, b))  # Expected: False
