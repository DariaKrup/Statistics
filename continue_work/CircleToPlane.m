% 2019-04-14
% draw projection circle to detector plane
% 2019-11-17 JCT Figure 16 black color
% 2019-12-14 color

% Load data from file.
clear;
close all;
filename = 'sol-35685-167-dsep.mat';
load(filename);
[m,n] = size(K);


% Create params for task.
cells_in_layer = 26;
cell_curr = 1;  % Start from first cell.
layers = 7;

for layer = 4:layers
    for cell_curr = 1 : cells_in_layer
        % Create array as 'delta-function'.
        test_sol = zeros(n, 1);
        test_sol(cell_curr + cells_in_layer * (layer - 1)) = 1;

        out = K * test_sol;
        out_reshape = reshape(out, 16, 16);
        outsq=out_reshape(16:-1:1, :);
        out_final=outsq(:, 16:-1:1);

        % Plot whole solution.
        % Part of meridional view.
        subplot(1,2,1);
        draw_solution(surfaces, segments, test_sol);
        axis('equal');
        xlim([-0.7 0.7]);
        ylim([-0.7 0.7]);
        xlabel('r, m');
        ylabel('z, m');
        title('Meridional view')

        % Part of detector view with rotation.
        subplot(1,2,2);
        pcolor(out_final);
        axis('equal');
        xlim([1 16]);
        ylim([1 16]);
        xlabel('column');
        ylabel('row');
        title('Detector view');
        
        title_str_name = strcat( {'Basic solution layer='}, num2str(layer), {' cell='}, num2str(cell_curr));
        suptitle(title_str_name);
        figure_name_out = char(title_str_name);
        path = 'C:\Users\Daria\Documents\Practise_FTI\code';
        saveas(gcf, fullfile(path, figure_name_out), 'png'); 
    end 
end
