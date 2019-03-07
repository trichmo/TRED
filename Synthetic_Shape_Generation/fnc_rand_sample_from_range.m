function sample = fnc_rand_sample_from_range(range)
range_min = min(range);
range_max = max(range);
sample = rand(1) * (range_max - range_min) + range_min;
