import math

def projectile_motion(v0=20.0, angle_deg=45.0, g=9.81):
    theta = math.radians(angle_deg)
    vx = v0 * math.cos(theta)
    vy = v0 * math.sin(theta)
    def pos(t):
        x = vx * t
        y = vy * t - 0.5 * g * t*t
        return x, y
    return pos

def pendulum_simulation(length=1.0, theta0=0.5, g=9.81):
    omega = math.sqrt(g/length)
    def theta(t):
        return theta0 * math.cos(omega * t)
    return theta
