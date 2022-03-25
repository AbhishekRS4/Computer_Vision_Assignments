function disparity=compute_disparity(left_image_gray, right_image_gray, window_size, method)
    image_shape = size(left_image_gray);
    %image_shape = size(right_image_gray);
    
    image_height = image_shape(1);
    image_width = image_shape(2);
    
    disparity = zeros(image_height, image_width);
    fprintf("Image size = %d %d\n", size(disparity));
    
    window_search_range = 19;
    disparity_scaling_factor = 16;
    
    if method == "absolute_diff"
        fprintf("Goodness fit measure - absolute difference\n");
        fprintf("window size = %d, window search range = %d\n", window_size, window_search_range);
    elseif method == "norm_cross_corr"
        fprintf("Goodness fit measure - normalized cross correlation\n");
        fprintf("window size = %d\n", window_size);
    end
    
    fprintf("Started computing disparity map\n");
    for y=window_size:(image_height-window_size-1)
    %for y=window_size:window_size
        for x=window_size:(image_width-window_size-1)
        %for x=window_size:window_size + 20
            left_image_patch = left_image_gray(y:y+window_size, x:x+window_size);
            if method == "absolute_diff"
                match_index_x = get_index_from_absolute_difference(y, x, left_image_patch, right_image_gray, image_width, window_size, window_search_range);
            elseif method == "norm_cross_corr"
                match_index_x = get_index_from_cross_correlation(y, x, left_image_patch, right_image_gray, image_width, window_size);
            end
            disparity(y, x) = abs(match_index_x - x);
        end 
    end
    disparity = uint8(disparity * disparity_scaling_factor);
    fprintf("finished computing disparity map\n");
end

function match_index_x_cc = get_index_from_cross_correlation(y, x, left_image_patch, right_image, image_width, window_size)
    x_min = 1;
    x_max = image_width;
    max_cc = 0;
    match_index_x_cc = 0;
    first_comparison = true;
    
    right_image_patch = right_image(y:y+window_size, x_min:x_max);
    cross_correlation = normxcorr2(left_image_patch, right_image_patch);
    %fprintf(cross_correlation);
    [y_peak, x_peak] = find(cross_correlation==max(cross_correlation(:)));
    
    %fprintf(size(cross_correlation));
    %fprintf(x_peak);
    match_index_x_cc = x_peak(1, 1) - window_size;
    %fprintf(match_index_x_cc);
end

function match_index_x_ab = get_index_from_absolute_difference(y, x, left_image_patch, right_image, image_width, window_size, window_search_range)
    x_min = x;
    x_max = min(image_width-window_size, x+window_search_range);
    min_error = 0;
    match_index_x_ab = 0;
    first_comparison = true;
    
    for x_index=x_min:x_max
        right_image_patch = right_image(y:y+window_size, x_index:x_index+window_size);
        sum_error = sum(abs(left_image_patch - right_image_patch), "all");
        if first_comparison == true
            min_error = sum_error;
            match_index_x_ab = x_index;
            first_comparison = false;
        else
            if sum_error < min_error
                min_error = sum_error;
                match_index_x_ab = x_index;
            end
        end
    end
end