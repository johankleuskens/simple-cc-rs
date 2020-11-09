import  matplotlib.pyplot as plt
import  math
import  numpy as np
import  scipy.special as sc

# Based on this URL: https://pwayblog.com/2016/07/03/the-clothoid/

def rotate(cx, cy, angle):
    s = np.sin(angle);
    c = np.cos(angle);

    xnew = cx * c - cy * s;
    ynew = cx * s + cy * c;

    return xnew, ynew;

# compute fresnel integral
# l : length
# A : ??
def fresnel (l, A):

    x = l - l**5/(40*A**4) + l**9/(3456*(A**8)) - l**13/(599040*(A**12))
    y = l**3/(6*(A**2)) - l**7/(336*(A**6)) + l**11/(42240*(A**10)) - l**15/(9676800*(A**14))
    return x,y

# Create a clothoid 
# l:         length of clothoid
# A:         curvature acceleration
# x0:        x offset coordinate
# y0:        y offset coordinate
# theta0:    offset angle
def create_clothoid(l, A, x0 = 0, y0 = 0, theta0 = 0, mirror = 0):
    # caculate various lengths
    t = np.linspace(0, l , 25)
    # correction to be compliant with URl shwon above
    corr = A * math.sqrt(math.pi)
    S, C = sc.fresnel(t / corr)
    
    if (mirror):
        c = x0 - np.array(C) * corr
    else:
        c = x0 + np.array(C) * corr
 
    s = y0 + np.array(S) * corr
    px, py = rotate(c, s, 0)
    
    return px,py
    
# Define constant A
A = 1000.0

# Minimum turning radius
R = 4.0

# define angle between two lines
alpha = 60.0/360.0*np.pi*2
#calculate gradient of the normal of the mid line
gr_m = np.tan(alpha/2+ math.pi/2)

# Calculate length at gradient of mid line
lrc = math.sqrt((math.pi/2-alpha/2) * (2 * A**2))
# Calculate length when minimum turning radius is reached
lr = (A**2)/R 
lr=lrc
# Calculate length of clothoid
lc = min(lrc, lr)

# calculate x and y coordinates of end of clothoid
corr = A * math.sqrt(math.pi)
ya,xa = sc.fresnel(lc / corr)
xa = xa * corr
ya = ya * corr
#calculate x coordinate of mid line where clothoid meets mid line
xb = ya/np.tan(alpha/2)

# plot the intersection of mid line and clothoid
plt.plot(xb, ya, 'ro')

# Create an array of lengths
#t = np.linspace(0, min(l90, lr) , 25)
# Calculate x and y coordinates for each length
#xy = [fresnel(tt, A) for tt in t]
# Subtract the x coordinates
#x = [val[0] for val in xy]
# Subtract the y coordinates
#y = [val[1] for val in xy]

c, s = create_clothoid(lc, A, x0=xa+xb, y0=0, theta0=0, mirror=True)

# plot the two lines
plt.plot([0,xa+xb], [0,0], 'b')
plt.plot([0,(xa+xb)*np.cos(alpha)], [0,(xa+xb)*np.sin(alpha)], 'b')
#plot the mid line
plt.plot([0,(xa+xb)*np.cos(alpha/2)], [0,(xa+xb)*np.sin(alpha/2)], 'b--')


# Calculate gradient of each point
#g = [math.tan(l**2/(2*(A**2))) for l in t]
#plt.plot(x, y, 'g')
plt.plot(c, s, 'r--')
plt.show()

print("Ready")

        