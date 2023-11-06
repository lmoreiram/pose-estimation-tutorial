# Function to compute angle
import numpy as np

def calculate_angle(v1, v2, joint):
    
    dot_product = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle_radians = np.arccos(np.clip(dot_product, -1.0, 1.0))  # Clip for stability
    angle_degrees = np.degrees(angle_radians)
    
    if joint == 'hip':
        angle_direction = -1 if v2[0]<0 else 1
    else:
        angle_direction = 1 
    
    angle = angle_direction*angle_degrees

    return angle