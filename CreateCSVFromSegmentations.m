pixels=[]
for i = 1:length(BoundaryList)
    segmentation = BoundaryList(i).PixelList;
    for j = 1:length(segmentation)
       region = segmentation{j};
       for k = 1:length(region)
          pixels = cat(1,pixels,region(k,2:3));
       end
       pixels = cat(1,pixels,[-1,-1]);
    end
end

csvwrite('imgSeg.csv',pixels);