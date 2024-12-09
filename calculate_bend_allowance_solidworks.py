from math import tan, pi, sqrt

def calculate_k_factor(thickness: float, radius: float) -> float:
    return 0.65 + 0.5 * sqrt(radius/thickness)

def calculate_bend_allowance(bend_angle: float, thickness: float, radius: float) -> float:
    if bend_angle >= 165 and bend_angle <= 180:
        raise ValueError("Bend angles between 165° and 180° are not possible with air bending")
    
    k = 0.65 + 0.5 * sqrt(radius/thickness)
    
    length = (pi * (180 - bend_angle)/180) * (radius + (k/2)*thickness) * 2
    
    if bend_angle < 90:
        length += thickness
    else:
        length *= tan((180 - bend_angle)/2)
    
    return length

def calculate_bend_allowance_with_radius_multiplier(bend_angle: float, thickness:float, bend_radius_multiplier: float) -> float:
    return calculate_bend_allowance(bend_angle, thickness, bend_radius_multiplier * thickness)