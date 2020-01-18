from math import pi, radians, degrees, sin, cos, atan, sqrt, sinh, cosh, asinh
import numpy as np
from scipy.integrate import quadrature
from scipy.optimize import newton
import matplotlib.pyplot as plt

# Parameters of projectile (Modelled after a baseball)
V_0     = 12.6                 # Initial velocity (m/s)
g       = 9.81                 # Acceleration due to gravity (m/s^2)
psi     = 1                   # Launch angle (deg.)
c       = 0.43                  # Drag coefficient (spherical projectile)
r       = 0.06               # Radius of projectile (m)
m       = 0.10                # Mass of projectile (kg)
rho_air = 1.45                 # Air density (kg/m^3)
a       = pi * r**2.0          # Cross-sectional area of projectile (m^2)
psi     = radians(psi)         # Convert to radians

# Initial position and launch velocity
x_0 = 0.0
u_0 = V_0 * cos(psi)
y_0 = 12
v_0 = V_0 * sin(psi)
# Constants and function definitions for solution
mu = 0.5 * c * rho_air * a / m
Q_0 = asinh(v_0 / u_0)
A   = g / (mu * u_0**2.0) + (Q_0 + 0.5 * sinh(2.0 * Q_0))

def lam(Q):
    return A - (Q + 0.5 * sinh(2.0 * Q))

def u_s(Q):
    return sqrt(g / mu) / sqrt(lam(Q))

def v_s(Q):
    return sqrt(g / mu) * sinh(Q) / sqrt(lam(Q))

def f_t(Q):
    return cosh(Q) / sqrt(lam(Q))

def f_x(Q):
    return cosh(Q) / lam(Q)

def f_y(Q):
    return sinh(2.0 * Q) / lam(Q)

def t_s(Q):
    return - quadrature(f_t, Q_0, Q, vec_func=False)[0] / sqrt(g * mu)

def x_s(Q):
    return x_0 - quadrature(f_x, Q_0, Q, vec_func=False)[0] / mu

def y_s(Q):
    return y_0 - quadrature(f_y, Q_0, Q, vec_func=False)[0] / (2.0 * mu)

def y_s_p(Q):
    return -(1.0 / (2.0 * mu)) * sinh(2.0 * Q) / lam(Q)

# Time of flight
def q_test():
    Q_T_est = asinh(-v_0 / u_0)
    return Q_T_est

def q_t():
    Q_T = newton(y_s, q_test(), y_s_p)
    return Q_T

def calc(height, speed):
    global y_0
    global v_0
    y_0 = height
    v_0 = speed
    R = x_s(q_t())
    return R

