function [xp, yp, totalArcLen] = fnc_get_perturbation(...
    run, rise, totalArcLen, noise_theta, noise_r, additional_noise)
% Modified from Turner's Python implementation

mag = sqrt(run^2 + rise^2);
totalArcLen = totalArcLen + mag;
dx = rise ./ mag;
dy = -run ./ mag;
% if isRandom == 1
%     perturb = normrnd(0, 0.3) * 0.1;
%     xp = dx .* perturb;
%     yp = dy .* perturb;
% else
xp = dx .* cos(totalArcLen .* noise_theta) .* (noise_r + additional_noise);
yp = dy .* cos(totalArcLen .* noise_theta) .* (noise_r + additional_noise);
% end
