function sample_2(window_size, method)
    file_left_img = "im2.ppm";
    file_right_img = "im8.ppm";
    gt_disparity = imread("disp2.pgm");
    
    left_image_gray = rgb2gray(imread(file_left_img));
    right_image_gray = rgb2gray(imread(file_right_img));
    
    if nargin > 1
        method = method; 
    else
        method = "absolute_diff";
    end
    
    disparity = compute_disparity(left_image_gray, right_image_gray, window_size, method);
    
    figure(1);
    %sgtitle("Disparity computation for stereo images");
    %subplot(2,2,1),imshow(left_image_gray),title("stereo left image");
    %subplot(2,2,2),imshow(right_image_gray),title("stereo right image");
    %subplot(1,2,1),imshow(gt_disparity),title("ground truth disparity map");
    
    % disparity scaling factor is actually 8, 
    % so divide disparity map by 2 since a factor of 16 was applied earlier
    subplot(1,1,1),imshow(disparity/2),title("computed disparity map");
end