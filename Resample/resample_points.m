function points = resample_points(data,delta_z,step_size_t)
data = prepare_data(data);
spline_resample = spline_resampling(data, delta_z);
points = circular_resampling(spline_resample,step_size_t);
end

