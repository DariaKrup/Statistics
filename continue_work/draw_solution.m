function [] = draw_solution(surfaces,segments, argmax)
    h = 0.0;
    
    draw_surfaces(surfaces, h);
    colormap parula;
    cmp = colormap;
    caxis([min(argmax) max(argmax)]);
    %colorbar();
    hold on;
    grid on;
    argma_length = max(argmax);% - min(argmax);
    for i = 1:length(segments)
        cl_ind = (argmax(i)) / argma_length;
        cl_ind = floor(cl_ind * (length(cmp) - 1));
        cl_ind = cl_ind + 1;
        if (argmax(i) < 0)
            cl_ind = 1;
        end
        argmax(i);
        segm = find_section(segments{i}, h);
        if (~isempty(segm))
            fill(segm(:, 1), segm(:, 2), cmp(cl_ind, 1:3)); 
            fill(-segm(:, 1), segm(:, 2), cmp(cl_ind, 1:3)); 
        end
    end
    %colorbar(argmax);
end

