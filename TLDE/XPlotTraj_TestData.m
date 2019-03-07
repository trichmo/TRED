% This script computes the dense version of the histogram of trajectories
% around a point using the test data used in the paper.
%
% Author: Edgar Lobaton

%% LOADING DATA
avg_time = 0;

obj_type = 'Ellipse';
data_type = 'perturbed';
%r2 = [0.15^2 0.3^2];
r2 = [0.3^2];
%thresholds = [1,5,10,15,20,25,50];
thresholds = [65,80];
% for j = 1:length(thresholds)
%     mkdir(strcat('C:/Users/trichmo/Data/TRED_Synthetic/',obj_type,'/dense/',num2str(thresholds(j)),'/'));
% end
% for img_idx = 1:200
%     D = load(strcat('C:/Users/trichmo/Data/TRED_Synthetic/',obj_type,'/GT/',int2str(img_idx),'_',data_type,'_0.csv'));
%     
%     for k = 1:length(r2)
%         tic
%         zG = getImg(D,r2(k));
%         avg_time = avg_time + toc;
%         for j = 1:length(thresholds)
%             imwrite(zG>=thresholds(j), strcat('C:/Users/trichmo/Data/TRED_Synthetic/',obj_type,'/dense/',num2str(thresholds(j)),'/',int2str(img_idx),'_',data_type,'_',num2str(r2(k)),'.png'))
%         end
%     end
% end
% 
% avg_time = avg_time / 200;

D = load(strcat('C:/Users/trichmo/Data/TRED_Synthetic/',obj_type,'/GT/','raw_0.csv'));
for k = 1:length(r2)
    zG = getImg(D,r2(k));
    %imwrite(zG>1, strcat('C:/Users/trichmo/Data/TRED_Synthetic/',obj_type,'/dense/','raw_',num2str(r2(k)),'.png')) 
end

