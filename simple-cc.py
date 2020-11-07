import  matplotlib.pyplot as plt
import  math
import  numpy as np
import  scipy.special as sc

# Based on this url: https://pwayblog.com/2016/07/03/the-clothoid/

# compute fresnel integral
# l : length
# A : ??
def fresnel (l, A):

    x = l - l**5/(40*A**4) + l**9/(3456*(A**8)) - l**13/(599040*(A**12))
    y = l**3/(6*(A**2)) - l**7/(336*(A**6)) + l**11/(42240*(A**10)) - l**15/(9676800*(A**14))
    return x,y

# Define constant A
A = 0.7

# Minimum turning radius
R = 4

# Calculate length at 90 degrees
l90 = math.sqrt(math.pi * A**2)

# Calculate length when minimum turning radius is reached
lr = (A**2)/R 

# Create an array of lengths
t = np.linspace(0, min(l90, lr) , 25)
# Calculate x and y coordinates for each length
xy = [fresnel(tt, A) for tt in t]
# Subtract the x coordinates
x = [val[0] for val in xy]
# Subtract the y coordinates
y = [val[1] for val in xy]

# Calculate fresnel integral via scipy function
corr = A*math.sqrt(math.pi)
S, C = sc.fresnel(t / corr)
s = np.array(S) * corr
c = np.array(C) * corr

# Calculate gradient of each point
g = [math.tan(l**2/(2*(A**2))) for l in t]
plt.plot(x, y, 'g')
plt.plot(c, s, 'r--')
plt.show()

print("Ready")

        