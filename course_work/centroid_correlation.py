import scipy.io as isc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
interval = [135.0, 175.0]


def get_data_from_file():
    all_variables = isc.loadmat('37000_SPD16x16.mat')
    data_array = np.rot90(all_variables.get("sign_bb"), 2)
    q_size = data_array.shape
    return data_array, all_variables, q_size


def prepare_extra_data(all_variables, main_matrix):
    data = all_variables.get("Data")
    dt = float(data[0, 1] * (10 ** (-3)))
    t_start = int((interval[0] - float(data[1, 1])) / dt)
    t_end = int((interval[1] - float(data[1, 1])) / dt)

    t = slice(t_start, t_end)
    matrix_up = main_matrix[:8, ...]
    matrix_low = main_matrix[8:, ...]

    return t, t_start, t_end, dt, matrix_up, matrix_low


if __name__ == '__main__':
    main_matrices, all_variables, indices = get_data_from_file()
    t, t_s, t_e, dt, B_up, B_low = prepare_extra_data(all_variables, main_matrices)

    sum_data = main_matrices.sum(axis=(0, 1))
    up_sum_data = B_up.sum(axis=(0, 1))
    low_sum_data = B_low.sum(axis=(0, 1))

    # The whole luminosity
    grid = np.linspace(interval[0], interval[0] + dt * len(up_sum_data), len(up_sum_data))
    sns.lineplot(grid, up_sum_data, label='Север', linewidth=1)
    sns.lineplot(grid, low_sum_data, label='Юг', linewidth=1)
    plt.title('Суммарная светимость')
    plt.xlabel('t, ms')
    plt.ylabel('luminosity values')
    plt.legend()
    plt.savefig('luminosity_whole.png', format='png')
    plt.show()

    # Common luminosity on interval
    grid = np.linspace(interval[0], interval[0] + dt * len(up_sum_data[t]), len(up_sum_data[t]))
    sns.lineplot(grid, up_sum_data[t], label='Север', linewidth=1)
    sns.lineplot(grid, low_sum_data[t], label='Юг', linewidth=1)
    plt.title('Суммарная светимость на заданном интервале')
    plt.xlabel('t, ms')
    plt.ylabel('luminosity values')
    plt.legend()
    plt.savefig('luminosity.png', format='png')
    plt.show()

    # Correlation coefficient of south and north
    cur_data = main_matrices[:, :, t]
    window = int(1 / dt)
    cur_data_up = main_matrices[8:, :, t].sum(axis=(0, 1))
    cur_data_down = main_matrices[:8, :, t].sum(axis=(0, 1))
    correlations = [np.corrcoef(cur_data_up[i:i + window], cur_data_down[i:i + window])[0, 1]
                    for i in range(cur_data.shape[-1] - window)]
    n = len(correlations)
    x_grid = np.linspace(interval[0], interval[0] + dt * n, n)
    plt.plot(x_grid, correlations, color='blue', linewidth=1)
    plt.title("Коэффициент корреляции между севером и югом")
    plt.ylabel('y')
    plt.xlabel('t, ms')
    plt.savefig('correlation.png', format='png')
    plt.show()

    # Find borders of area with huge deviation
    part_array = []
    for i in range(n):
        if correlations[i] <= 0.7:
            part_array.append(correlations[i])
    index_start_dev = correlations.index(part_array[0])
    index_end_dev = correlations.index(part_array[-1])



    # Centroid w/o normalization
    c_mass = [np.mean(np.array((np.mean(cur_data_up[i:i + window]), np.mean(cur_data_down[i:i + window]))))
              for i in range(cur_data.shape[-1] - window)]
    sns.lineplot(x_grid, c_mass, linewidth=1, color='deepskyblue', label='Траектория центра масс')
    plt.title('Движение центра масс без нормирования данных')
    plt.xlabel('t, ms')
    plt.ylabel('luminosity values')
    plt.legend()
    plt.savefig('centroid_wo_norm.png', format='png')
    plt.show()

    # Normalization
    d = {'y': pd.Series(c_mass)}
    df = pd.DataFrame(d)
    normalized_df = (df - df.min()) / (df.max() - df.min())

    # Centroid and corrcoef
    plt.plot(x_grid, correlations, linewidth=1, color='blue', label='Коэффициент корреляции')
    sns.lineplot(x_grid, normalized_df['y'], linewidth=1, color='deepskyblue', label='Траектория центра масс')
    plt.axvline(x=x_grid[index_start_dev], color='darkblue', linestyle='--', linewidth=0.5,
                label='Граница области')
    plt.axvline(x=x_grid[index_end_dev], color='darkblue', linestyle='--', linewidth=0.5)
    plt.title('Движение центра масс и коэффициент корреляции')
    plt.ylabel('y')
    plt.xlabel('t, ms')
    plt.legend()
    plt.savefig('centroid_norm.png', format='png')
    plt.show()

    # Find angle of line
    xdelta = np.diff(x_grid)
    ydelta = np.diff(c_mass)
    res = np.rad2deg(np.arctan2(ydelta, xdelta))
    index = []
    for i in range(len(res)):
        if res[i] < -89.995 and i > index_start_dev:
            index.append(i)
    for point in index:
        plt.scatter(x_grid[point], normalized_df['y'][point], color='blue', marker='o', s=3)
    plt.plot(x_grid, correlations, linewidth=1, color='blue', label='Коэффициент корреляции')
    sns.lineplot(x_grid, normalized_df['y'], linewidth=1, color='deepskyblue', label='Траектория центра масс')
    plt.axvline(x=x_grid[index_start_dev], color='darkblue', linestyle='--', linewidth=0.5,
                label='Граница области')
    plt.axvline(x=x_grid[index_end_dev], color='darkblue', linestyle='--', linewidth=0.5)
    plt.title('Точки, подозрительные на движение по вертикали, общий график')
    plt.legend()
    plt.savefig('points_vertical.png', format='png')
    plt.show()
    print('Angle:', np.round(np.min(res), decimals=5))



    # Correlation between deviations
    """dev_corr = [np.std(correlations[i:i + window]) for i in range(cur_data.shape[-1] - window)]
    dev_mass = [np.std(normalized_df['y'][i:i + window]) for i in range(cur_data.shape[-1] - window)]
    corr_coef = [np.corrcoef(dev_corr[i:i + window], dev_mass[i:i + window])[0, 1]
                    for i in range(cur_data.shape[-1] - window)]
    #plt.plot(x_grid, correlations, linewidth=1, color='dodgerblue', label='Коэффициент корреляции')
    #sns.lineplot(x_grid, normalized_df['y'], linewidth=1, color='lightskyblue',  label='Траектория центра масс')
    sns.lineplot(x_grid, corr_coef, linewidth=1, color='darkblue', linestyle='--', label='Корреляция величин')
    plt.title('Корреляция величин')
    plt.xlabel('t, ms')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('corr_values.png', format='png')
    plt.show()"""



