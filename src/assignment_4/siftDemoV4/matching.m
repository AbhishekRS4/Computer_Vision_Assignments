[num, locs, x_disp, y_disp] = match_disp('tsukuba1.pgm', 'tsukuba2.pgm');

% Remove those matches with a y_disp with larger than 1 (abs) as this
% cannot be correct.
idx = find(y_disp < 1 & y_disp > -1);

x_disp = x_disp(idx);

x_loc = locs(:, 2);
x_loc = x_loc(idx);
y_loc = locs(:, 1);
y_loc = y_loc(idx);


image = imread('tsukuba1.pgm');
[rows, cols] = size(image); 

z = zeros(rows, cols, "uint8");
for y = 1:rows
    for x = 1:cols
        % Find its closest sift feature (nearest neighbour using euclid)
        distances = (x_loc - x).^2 + (y_loc - y).^2;
        [minVal, argmin] = min(distances);
        z(y,x) = x_disp(argmin);
    end
end
figure
hold on
[M,c] = contourf(z);
colormap(gray(256));
set(gca, 'YDir','reverse')
scatter(x_loc, y_loc)
set(c,'LineColor','none')