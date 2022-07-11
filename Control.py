import numpy as np

I = 0
e = 0
e_0 = 0
Kp = 0.1
Ki = 0.1
Kd = 0.1
dt = 0.1
g = 9.87
scale = 1 / 60

def solve(x_0, theta_0, dx_0, setpoint, status):
    if status == "RESET":
        I = 0
        e = 0
    e_0 = e
    e = setpoint - x_0
    P = Kp * e
    I += Ki * e * dt
    D = Kd * (e - e_0) / dt
    u = P + I + D
    dtheta = scale * u
    if dtheta > 1:
        dtheta = 1
    theta = theta_0 + dtheta
    xdd = (5 * g / 7) * np.radians(theta)
    dx = dx_0 + dt * dt * xdd
    return dx, dtheta
