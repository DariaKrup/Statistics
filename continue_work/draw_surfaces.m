function [ ] = draw_surfaces( surfaces, h )
    hold on;
    grid on;
    axis( [ -0.7, 0.7, -0.7, 0.7 ] );

    for i = 1:length(surfaces)
        surf = find_section(surfaces{i}, h);
        
        if i == 1
            par = 'b';
        else
            par = 'g';
        end
        if (~isempty(surf))
            plot(surf(:, 1), surf(:, 2), par);
            plot(-surf(:, 1), surf(:, 2), par);
        end
    end
end

