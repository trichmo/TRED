function [zG] = getImg(D, r2)
%GETIMG Summary of this function goes here
%   Detailed explanation goes here
    xS{1} = D(:,1)';
    yS{1} = D(:,2)';

    %M = round(1.8*max(abs(D(:))));
    M=3;
    axis(M*[-1 1 -1 1]);

    %% PRODUCING COUNT IMAGE

    % Radius of support
    
    %r2 = [1.3^2 3.0^2];

    % Computing grid of points
    [xG,yG] = meshgrid(linspace(-M,M,500));

    % Initializing count matrix
    zG = zeros(size(xG));

    % Updating values in count matrix
    for n = 1:numel(xG)
        for i = 1:length(xS)
            idx = ((xS{i}-xG(n)).^2 + (yS{i}-yG(n)).^2)<r2;
            zG(n) = zG(n) + nnz(diff([0 idx])>0);
        end
    end
    %zG = log(zG+1);
end

