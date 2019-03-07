function [noisedX, noisedY] = fnc_add_noise_perperndicular(...
    waveX, waveY, pulseR, perturb_theta_range, perturb_r_range, isRandom)
% Modified from Turner's Python implementation
n_sample = length(waveX);

noisedX = [];
noisedY = [];
totalArcLen = 0;

if isRandom == 1
    noise_theta = fnc_rand_sample_from_range(perturb_theta_range);
    noise_r = fnc_rand_sample_from_range(perturb_r_range);
else
    noise_theta = 3.1;
    noise_r = 0.1;
end

for t = 1:n_sample
    if t==1
        run  = waveX(t+1) - waveX(t);
        rise = waveY(t+1) - waveY(t);
    else
        run  = waveX(t) - waveX(t-1);
        rise = waveY(t) - waveY(t-1);
    end
    [xp, yp, totalArcLen] = fnc_get_perturbation(...
        run,rise,totalArcLen, noise_theta, noise_r, pulseR(t));
    noisedX(t) = waveX(t) + xp;
    noisedY(t) = waveY(t) + yp;
end
