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
layer = 7;


% For separate cells in layer
for cell_curr = 1 : cells_in_layer
    % Create array as 'delta-function'.
    test_sol = zeros(n, 1);
    %for i = 1:8
    test_sol(cell_curr + cells_in_layer * (layer - 1)) = 1;
    %end
    out = K * test_sol;
    out_reshape = reshape(out, 16, 16);
    outsq=out_reshape(16:-1:1, :);
    out_final=outsq(:, 16:-1:1);

    % Plot whole solution.
    % Part of meridional view.
    hf_sub(1) = figure(1);
    hp(1) = uipanel('Parent', hf_sub(1), 'Position', [0 0 1 1]);
    subplot(1,2,1, 'Parent', hp(1));
    draw_solution(surfaces, segments, test_sol);
    axis('equal');
    xlim([-0.7 0.7]);
    ylim([-0.7 0.7]);
    xlabel('r, m');
    ylabel('z, m');
    title('Meridional view')

    % Part of detector view with rotation.
    subplot(1,2,2,'Parent', hp(1));
    pcolor(out_final);
    axis('equal');
    xlim([1 16]);
    ylim([1 16]);
    xlabel('column');
    ylabel('row');
    title('Detector view');

    full_title = strcat({'Layer'}, num2str(layer), {'cell = '},  num2str(cell_curr));
    suptitle(full_title);
        
    result = out_final;
    x = 1:1:64;
    %result = reshape(result', 1, m);

    hf_sub(2) = figure(2);
    hp(2) = uipanel('Parent', hf_sub(2), 'Position', [0 0 1 1]);
    %x = 65:1:128;
    subplot(2, 2, 1, 'Parent', hp(2));
    plot(x, reshape(result(9:16, 1:8), 1, 64));
    grid on;
    xlim([1 64]);
    ylim([-0.1 0.5]);
    xlabel('t');
    ylabel('sum values');
    title({'Second quarter'});



    subplot(2, 2, 2, 'Parent', hp(2));
    plot(x, reshape(result(9:16, 9:16), 1, 64));
    grid on;
    xlim([1 64]);
    ylim([-0.1 0.5]);
    xlabel('t');
    ylabel('sum values');
    title({'First quarter'});




    %x = 129:1:192;
    subplot(2, 2, 3, 'Parent', hp(2));
    plot(x, reshape(result(1:8, 1:8), 1, 64))
    grid on;
    xlim([1 64]);
    ylim([-0.1 0.5]);
    xlabel('t');
    ylabel('sum values');
    title({'Third quarter'});

    %x = 193:1:256;
    subplot(2, 2, 4, 'Parent', hp(2));
    plot(x, reshape(result(1:8, 9:16), 1, 64))
    grid on;
    xlim([1 64]);
    ylim([-0.1 0.5]);
    xlabel('t');
    ylabel('sum values');
    title({'Fourth quarter'});
    full_title = strcat({'Layer'}, num2str(layer), {'cell = '},  num2str(cell_curr));
    suptitle(full_title);

    hf_main = figure(3);
    npanels = numel(hp);
    hp_sub = nan(1, npanels);

    for idx=1:npanels
        hp_sub(idx) = copyobj(hp(idx), hf_main);
        set(hp_sub(idx), 'Position', [(idx-1)/npanels, 0, 1/npanels, 1]);
    end
    %title(full_title);
    path = 'C:\Users\Daria\Documents\Practise_FTI\code\fragment_w_graph';
    saveas(gcf, fullfile(path, char(full_title)), 'png'); 
end
 



% For full layer
% Create array as 'delta-function'.
test_sol = zeros(n, 1);
%for i = 1:8
for cell_curr =  1 : cells_in_layer
    test_sol(cell_curr + cells_in_layer * (layer - 1)) = 1;
end
    out = K * test_sol;
    out_reshape = reshape(out, 16, 16);
    outsq=out_reshape(16:-1:1, :);
    out_final=outsq(:, 16:-1:1);

    % Plot whole solution.
    % Part of meridional view.
    hf_sub(1) = figure(1);
    hp(1) = uipanel('Parent', hf_sub(1), 'Position', [0 0 1 1]);
    subplot(1,2,1, 'Parent', hp(1));
    draw_solution(surfaces, segments, test_sol);
    axis('equal');
    xlim([-0.7 0.7]);
    ylim([-0.7 0.7]);
    xlabel('r, m');
    ylabel('z, m');
    title('Meridional view')

    % Part of detector view with rotation.
    subplot(1,2,2,'Parent', hp(1));
    pcolor(out_final);
    axis('equal');
    xlim([1 16]);
    ylim([1 16]);
    xlabel('column');
    ylabel('row');
    title('Detector view');

    full_title = strcat({'Full layer '},  num2str(layer));
    suptitle(full_title);
        
    result = out_final;
    x = 1:1:64;
    %result = reshape(result', 1, m);

    hf_sub(2) = figure(2);
    hp(2) = uipanel('Parent', hf_sub(2), 'Position', [0 0 1 1]);
    %x = 65:1:128;
    subplot(2, 2, 1, 'Parent', hp(2));
    plot(x, reshape(result(9:16, 1:8), 1, 64));
    grid on;
    xlim([1 64]);
    ylim([-0.1 1]);
    xlabel('t');
    ylabel('sum values');
    title({'Second quarter'});



    subplot(2, 2, 2, 'Parent', hp(2));
    plot(x, reshape(result(9:16, 9:16), 1, 64));
    grid on;
    xlim([1 64]);
    ylim([-0.1 1]);
    xlabel('t');
    ylabel('sum values');
    title({'First quarter'});




    %x = 129:1:192;
    subplot(2, 2, 3, 'Parent', hp(2));
    plot(x, reshape(result(1:8, 1:8), 1, 64))
    grid on;
    xlim([1 64]);
    ylim([-0.1 1]);
    xlabel('t');
    ylabel('sum values');
    title({'Third quarter'});

    %x = 193:1:256;
    subplot(2, 2, 4, 'Parent', hp(2));
    plot(x, reshape(result(1:8, 9:16), 1, 64))
    grid on;
    xlim([1 64]);
    ylim([-0.1 1]);
    xlabel('t');
    ylabel('sum values');
    title({'Fourth quarter'});
    full_title = strcat({'Full layer '},  num2str(layer));
    suptitle(full_title);

    hf_main = figure(3);
    npanels = numel(hp);
    hp_sub = nan(1, npanels);

    for idx=1:npanels
        hp_sub(idx) = copyobj(hp(idx), hf_main);
        set(hp_sub(idx), 'Position', [(idx-1)/npanels, 0, 1/npanels, 1]);
    end
    %title(full_title);
    path = 'C:\Users\Daria\Documents\Practise_FTI\code\fragment_w_graph';
    saveas(gcf, fullfile(path, char(full_title)), 'png'); 

%path = 'C:\Users\Daria\Documents\Practise_FTI\code';
%saveas(gcf, fullfile(path, 'quarters'), 'png'); 
