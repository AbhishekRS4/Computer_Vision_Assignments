import numpy as np

def compute_focal_length_from_vanishing_points(vp_1, vp_2):
    focal_length = np.sqrt(-(np.sum(np.multiply(vp_1, vp_2))))
    return focal_length

def compute_vanishing_point(line_1_params, line_2_params):
    vp_x = - (line_1_params[1] - line_2_params[1]) / (line_1_params[0] - line_2_params[0])
    vp_y = line_1_params[0] * vp_x + line_1_params[1]
    return np.array([vp_x, vp_y])

def compute_line_params(line):
    # Use first two lines to compute the equation of the lines
    line_x = line[[0, 2]].reshape(-1)
    line_y = line[[1, 3]].reshape(-1)

    return np.polyfit(line_x, line_y, 1)

def parlines(lines, focal_length=1):
    n = 3 # get 3 dimensions
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
    wvec[0:2] /= focal_length
    wvec /= np.linalg.norm(wvec)

    return wvec

def read_lines_numpy_data(file_npy):
    line_arr = np.load(file_npy)
    return line_arr

def main():
    line_1 = read_lines_numpy_data("par_lines_1.npy")
    line_2 = read_lines_numpy_data("par_lines_2.npy")

    par_set_1_line_1 = compute_line_params(line_1[0])
    par_set_1_line_2 = compute_line_params(line_1[1])
    vp_1 = compute_vanishing_point(par_set_1_line_1, par_set_1_line_2)
    print("\nVanishing point for parallel lines set 1")
    print(vp_1)

    par_set_2_line_1 = compute_line_params(line_2[0])
    par_set_2_line_2 = compute_line_params(line_2[1])
    vp_2 = compute_vanishing_point(par_set_2_line_1, par_set_2_line_2)
    print("\nVanishing point for parallel lines set 2")
    print(vp_2)

    focal_length = compute_focal_length_from_vanishing_points(vp_1, vp_2)
    print(f"\nFocal length : {focal_length}")

    w_vec_line_1 = parlines(line_1, focal_length)
    w_vec_line_2 = parlines(line_2, focal_length)

    print("\nDirection vector of side 1 of rectangle")
    print(w_vec_line_1)
    print("\nDirection vector of side 2 of rectangle")
    print(w_vec_line_2)


    dot_product = np.dot(w_vec_line_1, w_vec_line_2)
    print(f"\nDot product : {dot_product}, should be close to 0 since the 2 sides of the rectangle are orthogonal")

    normal_vector = np.cross(w_vec_line_1, w_vec_line_2)
    print("\nNormal of planar patch containing the rectangle")
    print(normal_vector)

    return

main()
