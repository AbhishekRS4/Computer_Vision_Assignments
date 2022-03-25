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
    sgtitle("Disparity computation for stereo images");
    subplot(2,2,1),imshow(left_image_gray),title("stereo left image");
    subplot(2,2,2),imshow(right_image_gray),title("stereo right image");
    subplot(2,2,3),imshow(gt_disparity),title("ground truth disparity map");
    subplot(2,2,4),imshow(disparity),title("computed disparity map");
end