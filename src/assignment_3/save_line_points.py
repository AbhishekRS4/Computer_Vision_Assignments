import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from itertools import combinations

def parlines(lines):
    n = 3 # get 3 dimensions
    f = 1 #temporary
    a = np.zeros((lines.shape[0], n)) # some magic from parlines.m (tested and works)
    a[:,0] = lines[:,3] - lines[:,1]
    a[:,1] = -1*(lines[:,2] - lines[:,0])
    a[:,2] = np.multiply(lines[:,1], -1*a[:,1]) - np.multiply(lines[:,0],a[:,0])

    u, s, v = np.linalg.svd(a) # call matlab numpy routine

    if (v[2] < 0).all(): # s and v are already sorted from largest to smallest
        v_min = np.abs(v[2])
    else:
        v_min = v[2]

    wvec = v_min.T
    wvec[0:2] /= f
    wvec /= np.linalg.norm(wvec)

    return wvec

def onclick(event):
    global first_set
    if event.button == 3: # right click
        first_set = False

    if event.button == 1: # mouse click for first set
        if first_set:
            x.append(event.xdata) # store x and y for the clicked point
            y.append(event.ydata)
        else:
            x2.append(event.xdata)
            y2.append(event.ydata)
    for i in range(0, len(x), 2): # plot lines between points pairs
        ax.plot(x[i:i+2], y[i:i+2], 'ro-')
    for i in range(0, len(x2), 2): # plot lines between points pairs
        ax.plot(x2[i:i+2], y2[i:i+2], 'bo-')

    fig.canvas.draw()

if __name__ == "__main__":

    img = Image.open('rectangle.tif') # read the suppllied image

    x, y = [], [] # lists where the xs and ys of the first set of lines are stored
    x2, y2 = [], [] # lists for the orthogonal lines

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.imshow(img.rotate(180), origin='lower', cmap='gray') # set the axis-origin to lower for better understandability (and rotate image)
    first_set = True

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    print("""Click twice on the figure to create a line between two points. You can do this as many times for the number of parallel lines you want to include.
Once you are done with the first set, click once on the right mouse button to start selecting the lines for the second set.

The two sets should appear in red and blue.  When one is finished the window can be closed. """)

    plt.show()

  # Calculate camera constant (calculate first the vanishing points), the direction vectors and normal plane.

   # The following lines are useful to use the parfile.m function
    lines = np.array([x, y]).T.reshape((len(x) // 2, 4)) # reshape to ((x,y), (x,y)) per line
    lines2 = np.array([x2, y2]).T.reshape((len(x2) //2 , 4)) # reshape to ((x,y), (x,y)) per line
    np.save("par_lines_1.npy", lines)
    np.save("par_lines_2.npy", lines2)
