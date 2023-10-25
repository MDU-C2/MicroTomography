function DisplayMesh(meshEdges)
% Takes in a mesh, and displays it in a figure window inputs:
% meshEdges - a cell array, where each cell holds two points that represent
% an edge on the surface mesh

[numEdges, ~] = size(meshEdges);
% ptBoth=zeros(4,3);
figure;
hold on;
for i=1:numEdges
    pts = meshEdges{i};
    [~,dim] = size(pts);
    if(dim==2)
        plot(pts(:,1),pts(:,2))
    end 
    if (dim == 3)
    plot3(pts(:,1),pts(:,2),pts(:,3), 'color', 'black');
   end 
end
meshEdgesMat = cell2mat(meshEdges);
%%%% The shape that is outputed by the powercrust using alpha Shape.
 if(dim==3)
    shp = alphaShape(meshEdgesMat(:,1),meshEdgesMat(:,2),meshEdgesMat(:,3));
    shape.alpha = 200; 
    figure;
    plot(shp);
    hold off;
 else
    shp = alphaShape(meshEdgesMat(:,1),meshEdgesMat(:,2));
    shape.alpha = 200; 
    figure;
    plot(shp);
    hold off;
 end

end

