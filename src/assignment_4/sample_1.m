function sample_1(window_size, method)
    file_left_img = "scene1.row3.col4.ppm";
    file_right_img = "scene1.row3.col3.ppm";
    gt_disparity = imread("truedisp.row3.col3.pgm");
    
    left_image_gray = rgb2gray(imread(file_left_img));
    right_image_gray = rgb2gray(imread(file_right_img));
    
    if nargin > 1
        method = method; 
    else
        method = "absolute_diff";
    end
    
    disparity = compute_disparity(left_image_gray, right_image_gray, window_size, method);
    
    figure(1);
    subplot(2,2,1),
    imshow(left_image_gray);
    subplot(2,2,2),
    imshow(right_image_gray);
    subplot(2,2,3),
    imshow(gt_disparity);
    subplot(2,2,4),
    imshow(gt_disparity);
    
    figure(2);
    subplot(1,2,1),
    imshow(disparity);
    subplot(1,2,2),
    imshow(gt_disparity);
end