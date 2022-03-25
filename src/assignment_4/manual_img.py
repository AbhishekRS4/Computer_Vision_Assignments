import matplotlib.pyplot as plt

import numpy as np

im1 = 'scene1.row3.col3.ppm'
im2 = 'scene1.row3.col4.ppm'
gt_im = 'truedisp.row3.col3.pgm'

scaling_fac = 16

points_1 = [(280, 144), (174, 170), (118, 88), (345, 212), (98, 220)]
points_2 = [(266, 144), (163, 170), (112, 88), (337, 212), (93, 220)]

# points_1 = np.array(points_1)
# points_2 = np.array(points_2)

img1 = plt.imread(im1)
img2 = plt.imread(im2)

cmap = plt.cm.get_cmap('tab10')

plt.imshow(img1)
for i, point in enumerate(points_1):
    plt.scatter(point[0], point[1], color=cmap(i), s=100, edgecolors='white')
plt.tight_layout()
plt.savefig("manual_1.svg")
plt.show()

plt.imshow(img2)
for i, point in enumerate(points_2):
    plt.scatter(point[0], point[1], color=cmap(i), s=100, edgecolors='white')
plt.tight_layout()
plt.savefig("manual_2.svg")
plt.show()

points_1 = np.array(points_1)
points_2 = np.array(points_2)

disparities = points_1[:, 0] - points_2[:, 0]
print(disparities)


gt_img = plt.imread(gt_im)
plt.figure(figsize=(6.4, 5.5))
pos = plt.imshow(gt_img, cmap="gray")
plt.colorbar(pos, shrink=0.8, fraction=0.08, pad=0.10,
             orientation='horizontal', label='disparity')
plt.tight_layout()
plt.savefig("gt.png")
plt.show()

gt_disparities = []
for point in points_1:
    gt_disparities.append(gt_img[point[1], point[0]]/16)
print(gt_disparities)
