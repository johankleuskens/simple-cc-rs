import  matplotlib.pyplot as plt
import  math
import  numpy as np
import  scipy.special as sc

# Author: Johan Kleuskens (johan.kleuskens@phact.nl)
# Date : 11-11-2020

# Based on this URL: https://pwayblog.com/2016/07/03/the-clothoid/

def rotate(px, py, angle):
    s = np.sin(angle);
    c = np.cos(angle);

    xnew = px * c - py * s;
    ynew = px * s + py * c;

    return xnew, ynew;

# Create a clothoid 
# l:         length of clothoid
# A:         curvature acceleration
# x0:        x offset coordinate
# y0:        y offset coordinate
# theta0:    offset angle
# reverse:   go in opposite direction
# flip:     flip along x axis
def create_clothoid(l, A, x0 = 0, y0 = 0, theta0 = 0, reverse = False):
    # calculate various lengths
    t = np.linspace(0, l , 25)
    # correction to be compliant with URl shwon above
    corr = A * math.sqrt(math.pi)
    S, C = sc.fresnel(t / corr)

    c, s = rotate(C, S, theta0)             
    
    if (reverse):
        c = x0 - np.array(c) * corr
    else:
        c = x0 + np.array(c) * corr
 
    s = y0 + np.array(s) * corr
    px, py = rotate(c, s, 0)
    
    return px,py

def create_circle(R, x0, y0, arc, angle):
    # compute 10 points
    arcs = np.linspace(0, arc, 10)
    x = R * np.cos (arcs)
    y = R * np.sin(arcs)
    
    xr, yr = rotate(x, y, angle) 
    return xr+x0, yr+y0

sigma = 0.2

# Define constant A
A = 1/math.sqrt(sigma)

# Minimum turning radius
R = 4.0

# define angle between two lines
alpha = 90.0/360.0*np.pi*2

# Calculate length at gradient of mid line
lrc = math.sqrt((math.pi/2-alpha/2) * (2 * A**2))
# Calculate length when minimum turning radius is reached
lr = (A**2)/R 

# Calculate length of clothoid
lc = min(lrc, lr)

# calculate x and y coordinates of end of clothoid
corr = A * math.sqrt(math.pi)
ya,xa = sc.fresnel(lc / corr)
xa = xa * corr
ya = ya * corr
#calculate angle at end of clothoid
beta = math.pi/2 - lc**2/(2 * A**2)


# calculate coordinate of center point of circle
dyb = R * np.sin(beta)
dxb = R * np.cos(beta)
ry = ya + dyb
rx = ry/np.tan(alpha/2)
xb = rx-dxb
plt.plot(rx, ry, 'ro')

# calculate arc length of cirle
gamma = beta - alpha/2

xc, yc = create_circle(R, rx, ry, arc=2*gamma, angle=beta - 2*gamma - math.pi)
plt.plot(xc, yc, 'g')

# show an arrow for the gradient at the end of the  first clothoid
# plt.arrow(xb, ya, 10*math.cos(beta), 10*math.sin(beta))

# calculate first clothoid
cf, sf = create_clothoid(lc, A, x0=xa+xb, y0=0, theta0=0, reverse=True)

# calculate start point of second clothoid
xas = (xa+xb)*np.cos(alpha)
yas = (xa+xb)*np.sin(alpha)
cs, ss = create_clothoid(lc, A, x0=xas, y0=yas, theta0=alpha-math.pi)

# plot the two lines
plt.plot([0,xa+xb], [0,0], 'b')
plt.plot([0,xas], [0,yas], 'b')
#plot the mid line
plt.plot([0,(xa+xb)*np.cos(alpha/2)], [0,(xa+xb)*np.sin(alpha/2)], 'b--')


# Calculate gradient of each point
#g = [math.tan(l**2/(2*(A**2))) for l in t]
#plt.plot(x, y, 'g')
plt.plot(cf, sf, 'r--')
plt.plot(cs, ss, 'r--')
plt.show()

print("Ready")

        