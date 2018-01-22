figure;
hold on;

numPoints = 0;
for i = 1:32
    segmentation = BoundaryList(i).PixelList;
    for j = 1:length(segmentation)
       region = segmentation{j};
       numPoints = numPoints + length(region);
       numPoints = numPoints+1;
    end
end
pixels= zeros(numPoints,2);
nextRow = 1
for i = 1:32
    i
    segmentation = BoundaryList(i).PixelList;
    for j = 1:length(segmentation)
       region = segmentation{j};
       for k = 1:size(region,1)
          pixels(nextRow,:) = region(k,2:3);
          nextRow = nextRow+1;
       end
       scatter(region(:,2),region(:,3),'.');
       pixels(nextRow,:) = [-1,-1];
       nextRow = nextRow+1;
    end
end
hold off;

csvwrite('imgSeg.csv',pixels);