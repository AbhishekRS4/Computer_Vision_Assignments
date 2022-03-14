import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def compute_focal_length_from_vanishing_points(vp_1, vp_2):
    focal_length = np.sqrt(-(np.sum(np.multiply(vp_1, vp_2))))
    return focal_length


def compute_vanishing_point(line_1_params, line_2_params):
    vp_x = - (line_1_params[1] - line_2_params[1]) / \
        (line_1_params[0] - line_2_params[0])
    vp_y = line_1_params[0] * vp_x + line_1_params[1]
    return np.array([vp_x, vp_y])


def compute_vanishing_point_lstsq(line_coefs):
    line_coefs = np.array(line_coefs)
    # y = a*x + b
    a = line_coefs[:, 0]
    b = line_coefs[:, 1]

    # [-a_n, 1] * [x,y]^T = b_n
    coef = np.stack([-a, np.ones(len(a))], axis=1)

    # Solve for minimizing ||b - [-a, 1] * [x,y]^T||
    res = np.linalg.lstsq(coef, b, rcond=None)

    return res[0]


def compute_line_params(line):
    # Use first two lines to compute the equation of the lines
    line_x = line[[0, 2]].reshape(-1)
    line_y = line[[1, 3]].reshape(-1)

    return np.polyfit(line_x, line_y, 1)


def parlines(lines, focal_length=1):
    n = 3  # get 3 dimensions
    # some magic from parlines.m (tested and works)
    a = np.zeros((lines.shape[0], n))
    a[:, 0] = lines[:, 3] - lines[:, 1]
    a[:, 1] = -1*(lines[:, 2] - lines[:, 0])
    a[:, 2] = np.multiply(lines[:, 1], -1*a[:, 1]) - \
        np.multiply(lines[:, 0], a[:, 0])

    u, s, v = np.linalg.svd(a)  # call matlab numpy routine

    if (v[2] < 0).all():  # s and v are already sorted from largest to smallest
        v_min = np.abs(v[2])
    else:
        v_min = v[2]

    wvec = v_min.T
    wvec[0:2] /= focal_length
    wvec /= np.linalg.norm(wvec)

    return wvec


def read_lines_numpy_data(file_npy):
    line_arr = np.load(file_npy)
    return line_arr


def plot_intersection(centers, lines_l, par_lines_l, colors=['red', 'blue']):
    img = Image.open('rectangle.tif')
    plt.imshow(img.rotate(180), origin='lower', cmap='gray')

    intersects = []
    for lines, par_lines, color in zip(lines_l, par_lines_l, colors):
        # Plot all the lines
        for line in lines:
            plt.axline(line[:2], line[2:], color=color)

        # Plot all intersections
        n_lines = len(par_lines)
        for i in range(n_lines):
            for j in range(i + 1, n_lines):
                intersect = compute_vanishing_point(par_lines[i], par_lines[j])
                intersects.append(intersect)
       
    intersects = np.array(intersects)
    plt.scatter(intersects[:, 0], intersects[:, 1],
                c='tab:green', zorder=2, label='Pair-wise')

    # Plot the lstsq intersection
    centers = np.array(centers)
    plt.scatter(centers[:,0], centers[:,1], c='tab:red',
                zorder=3, label="Least squares")

    plt.axline(centers[0], centers[1], ls='dashed', label='Vanishing line')


    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    line_1 = read_lines_numpy_data("par_lines_1.npy")
    line_2 = read_lines_numpy_data("par_lines_2.npy")

    # par_set_1_line_1 = compute_line_params(line_1[0])
    # par_set_1_line_2 = compute_line_params(line_1[1])
    # vp_1 = compute_vanishing_point(par_set_1_line_1, par_set_1_line_2)

    par_set_1_lines = [compute_line_params(x) for x in line_1]
    vp_1 = compute_vanishing_point_lstsq(par_set_1_lines)
    print("\nVanishing point for parallel lines set 1")
    print(vp_1)

    # par_set_2_line_1 = compute_line_params(line_2[0])
    # par_set_2_line_2 = compute_line_params(line_2[1])
    # vp_2 = compute_vanishing_point(par_set_2_line_1, par_set_2_line_2)

    par_set_2_lines = [compute_line_params(x) for x in line_2]
    vp_2 = compute_vanishing_point_lstsq(par_set_2_lines)
    print("\nVanishing point for parallel lines set 2")
    print(vp_2)

    plot_intersection([vp_1, vp_2], [line_1, line_2], [par_set_1_lines, par_set_2_lines])

    focal_length = compute_focal_length_from_vanishing_points(vp_1, vp_2)
    print(f"\nFocal length : {focal_length}")

    w_vec_line_1 = parlines(line_1, focal_length)
    w_vec_line_2 = parlines(line_2, focal_length)

    print("\nDirection vector of side 1 of rectangle")
    print(w_vec_line_1)
    print("\nDirection vector of side 2 of rectangle")
    print(w_vec_line_2)

    dot_product = np.dot(w_vec_line_1, w_vec_line_2)
    print(
        f"\nDot product : {dot_product}, should be close to 0 since the 2 sides of the rectangle are orthogonal")

    normal_vector = np.cross(w_vec_line_1, w_vec_line_2)
    print("\nNormal to the planar patch containing the rectangle")
    print(normal_vector)

    return


main()
