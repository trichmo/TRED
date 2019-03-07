% This scripts generate curves with perturbations.
%
% Also several Gaussian pulses are uniformaly added to
% perturbation.
%
% Author: Qian Ge
% Date Created: 10/25/2018

% Number of periods (N/2) of the generated curve
N = 200;
% Number of sample points for generation
n_sample = 100000;
% Whether Randomly pick parameters for noise free curve or not 
is_random_perturbation = 1;
% Type of curve
type = 'circle';

% Setting parameters for each type of curve
if strcmp(type, 'eight')
    perturb_theta_range = [1, 3.1];
    perturb_r_range = [0.02, 0.07];
elseif strcmp(type, 'peanut')
    perturb_theta_range = [1, 3.1];
    perturb_r_range = [0.02, 0.07];
elseif strcmp(type, 'ellipse')
    perturb_theta_range = [1, 3.1];
    perturb_r_range = [0.02, 0.07];
else
    perturb_theta_range = [2, 5];
    perturb_r_range = [0.05, 0.1];
end

% Setting parameters for pulses
% range of number of pulses for a single circle
n_pulse_range = [10, 80];
% range of pulse standard derivation
pulse_sigma_range = [20, 30];
% range of magnitude of pulse
pulse_magnitude_range = [0.1, 0.5];

% Create noise free curve
[x, y] = fnc_curve_generator(N, n_sample, type);
for i = 1:200
    % Get random pulse
    pulse = fnc_get_pulse(...
        n_sample, n_pulse_range, pulse_sigma_range, pulse_magnitude_range);
    % Get noisy curve
    [noisedX, noisedY] = fnc_add_noise_perperndicular(...
        x, y, pulse, perturb_theta_range, perturb_r_range, is_random_perturbation);

    %% Draw curves
    % figure(1);clf
    % 
    % subplot(2,1,1)
    % plot(pulse)
    % title('Pulse')
    % axis([ 0, n_sample, -pulse_magnitude_range(1) * 2, pulse_magnitude_range(1) * 2])
    % 
    % subplot(2,1,2)
    % plot(noisedX, noisedY); axis equal;
    % title('Noisy Curve')
    
    %csvwrite(strcat('C:/Users/trichmo/Data/TRED_Synthetic/',type,'/','GT/',int2str(i),'_perturbed_0.csv'),[noisedX;noisedY]')
end
%csvwrite(strcat('C:/Users/trichmo/Data/TRED_Synthetic/',type,'/','GT/','/raw_0.csv'),[x;y]')

