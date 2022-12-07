function data = prepare_data(data)
%% Prepare data by filling the nan values of the short columns by values from longer columns. 
% find longest column 
[A,I] = min(min(sum(isnan(data))));

for i = 1:size(data,3)
    % create nan index
    nan_indexes = zeros(size(data,1),1,'logical');
    % find nan values
    nan_indexes(5:end)  = isnan(data(5:end,1,i)); % Skip first 5 values because sometimes nan values may be first in the column 
    % replace nan values with longest column 
    data(nan_indexes,:,i) = data(nan_indexes,:,I);
end
end

