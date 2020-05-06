import scipy.io as isc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.ndimage.measurements as meas
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

    # Common luminosity on time
    sns.lineplot(range(len(up_sum_data[t])), up_sum_data[t], label='Север')
    sns.lineplot(range(len(low_sum_data[t])), low_sum_data[t], label='Юг')
    plt.title("Суммарная светимость на заданном интервале")
    plt.legend()
    plt.savefig('luminosity.png', format='png')
    plt.show()

    cur_data = main_matrices[:, :, t]
    window = int(1 / dt)
    cur_data_up = main_matrices[8:, :, t].sum(axis=(0, 1))
    cur_data_down = main_matrices[:8, :, t].sum(axis=(0, 1))
    correlations = [np.corrcoef(cur_data_up[i:i + window], cur_data_down[i:i + window])[0, 1]
                    for i in range(cur_data.shape[-1] - window)]
    n = len(correlations)
    x_grid = np.linspace(interval[0], interval[0] + dt * n, n)
    plt.plot(x_grid, correlations, color='blue')
    plt.title("Коэффициент корреляции между севером и югом")
    plt.savefig('correlation.png', format='png')
    plt.show()

    part_array = []
    for i in range(n):
        if correlations[i] <= 0.5:
            part_array.append(correlations[i])
    index_start_dev = correlations.index(part_array[0])
    index_end_dev = correlations.index(part_array[-1])
    c_mass = [np.mean(np.array((np.mean(cur_data_up[i:i+window]), np.mean(cur_data_down[i:i+window]))))
              for i in range(cur_data.shape[-1] - window)]
    print(c_mass)
    #x = [c_mass[i][0] for i in range(len(c_mass))]
    #y = [c_mass[i][1] for i in range(len(c_mass))]
    #plt.plot(np.linspace(interval[0], interval[0] + dt * n, n), correlations)
    sns.lineplot(x_grid, c_mass, linewidth=1, color='deepskyblue', label='Траектория центра масс')
    max_tr = np.max(c_mass)
    index = c_mass.index(max_tr)
    #plt.scatter(x_grid[index], max_tr, color='orange', marker='o', s=15)
    plt.axvline(x=x_grid[index_start_dev], color='midnightblue',linestyle='--', linewidth=0.5,
                label='Граница области')
    plt.axvline(x=x_grid[index_end_dev], color='midnightblue', linestyle='--', linewidth=0.5)
    plt.title('Движение центра масс')
    plt.legend();
    plt.savefig('centroid.png', format='png')
    plt.show()
