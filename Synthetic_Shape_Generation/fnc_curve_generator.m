function [x, y] = fnc_curve_generator(N, n_sample, type)
% Modified from Turner's Python implementation
t = linspace(0, N*pi, n_sample);
if strcmp(type, 'eight')
    x = cos(t) ./ (sin(t).*sin(t) + 1);
    y = cos(t) .* sin(t) ./ (sin(t).*sin(t) + 1);
elseif strcmp(type, 'peanut')
    a = 0.92;
    b = 1;
    x = cos(t) .* sqrt((a.^2) .* cos(2 .* t) + sqrt(b.^4 + a.^2 .* sin(2 .* t).^2)) ./ 1.35883;
    y = sin(t) .* sqrt((a.^2) .* cos(2 .* t) + sqrt(b.^4 + a.^2 .* sin(2 .* t).^2));
elseif strcmp(type, 'ellipse')
    x = cos(t);
    y = sin(t);
    y = y ./ 2;
else
    x = cos(t);
    y = sin(t);
end