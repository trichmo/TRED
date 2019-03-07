function pulse = fnc_get_pulse(len_sample, n_pulse_range, pulse_sigma_range, magnitude_range)
x_axis = 1:len_sample;
n_pulse = randi(n_pulse_range);
pulse = 0;
disp(['[number of pulse]: ', num2str(n_pulse)])
for pulse_id = 1:n_pulse
    mu_id = randi(len_sample);
    mu = x_axis(mu_id);
    sigma = fnc_rand_sample_from_range(pulse_sigma_range);
    r = fnc_rand_sample_from_range(magnitude_range);
    pulse = pulse +2*((rand()>0.5)-0.5)*normpdf(x_axis, mu, sigma) ./ normpdf(mu, mu, sigma) .* r;
    
    disp(['** pulse ' num2str(pulse_id) ' **']);
    disp(['[mu, sigma]: ', num2str(mu), ' ', num2str(sigma)])
    disp(['[pulse r]: ', num2str(r)])
end