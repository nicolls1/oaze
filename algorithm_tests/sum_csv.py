import csv
import decimal
import math
from multiprocessing import Process, Queue, Manager
import time

import dask.dataframe as dd
from dask.distributed import Client, progress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read_file(file_name):
    with open(file_name) as csv_file:
        for row in csv_file:
            pass


def read_file_split(file_name):
    with open(file_name) as csv_file:
        for row in csv_file:
            row.strip().split(',')


def read_file_csv(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        headers = next(reader)
        for row in reader:
            pass


def read_file_pandas(file_name):
    file_data = pd.read_csv(file_name)


def sum_csv_int(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        headers = next(reader)
        amount_eur_index = headers.index('amount EUR')

        total = 0
        for row in reader:
            # Numbers always have 2 values to the right of the decimal so this should be safe.
            total += int(row[amount_eur_index][:-3]+row[amount_eur_index][-2:])

    str_sum = str(total)
    return f'{str_sum[:-2]}.{str_sum[-2:]}'


def sum_csv_int_comprehension(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        headers = next(reader)
        amount_eur_index = headers.index('amount EUR')

        values = [int(row[amount_eur_index][:-3]+row[amount_eur_index][-2:])
                  for row in reader]

    total = sum(values)
    str_sum = str(total)
    return f'{str_sum[:-2]}.{str_sum[-2:]}'


def sum_csv_fsum(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        headers = next(reader)
        amount_eur_index = headers.index('amount EUR')

        numbers = [float(row[amount_eur_index]) for row in reader]

    return '{:.2f}'.format(math.fsum(numbers))


def sum_csv_decimal(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        headers = next(reader)
        amount_eur_index = headers.index('amount EUR')
        numbers = [decimal.Decimal(row[amount_eur_index]) for row in reader]
    return str(sum(numbers))


def sum_split_int(file_name):
    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')

        total = 0
        for row in csv_file:
            string_value = row.strip().split(',')[amount_eur_index]
            # Numbers always have 2 values to the right of the decimal so this should be safe.
            total += int(string_value[:-3]+string_value[-2:])

    str_sum = str(total)
    return f'{str_sum[:-2]}.{str_sum[-2:]}'


def sum_split_int_comprehension(file_name):
    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')

        values = [int(row.strip().split(',')[amount_eur_index][:-3]+row.strip().split(',')[amount_eur_index][-2:])
                  for row in csv_file]

    total = sum(values)
    str_sum = str(total)
    return f'{str_sum[:-2]}.{str_sum[-2:]}'


def sum_split_fsum(file_name):
    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')

        numbers = [float(row.strip().split(',')[amount_eur_index]) for row in csv_file]
    return '{:.2f}'.format(math.fsum(numbers))


def sum_split_decimal(file_name):
    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')
        numbers = [decimal.Decimal(row.strip().split(',')[amount_eur_index]) for row in csv_file]
    return str(sum(numbers))


def sum_pandas(file_name):
    file_data = pd.read_csv(file_name)
    total = file_data['amount EUR'].sum()
    return '{:.2f}'.format(total)


def sum_dask_pandas(file_name):
    # Starts a dask local cluster with 2 workers/processes, running on a 4 core machine, used in dask pandas
    client = Client(n_workers=2, threads_per_worker=1, memory_limit='1GB')

    df = dd.read_csv(file_name)
    return '{:.2f}'.format(df['amount EUR'].sum().compute())


def do_work_group(in_queue, out_list):
    while True:
        amount_eur_index, lines = in_queue.get()

        # exit signal
        if lines is None:
            return

        result = [float(line.strip().split(',')[amount_eur_index]) for line in lines]

        out_list.append(math.fsum(result))


def sum_multiprocess_group_1000(file_name):
    num_workers = 2
    pool = []
    manager = Manager()
    results_list = manager.list()
    in_queue = Queue()
    for i in range(num_workers):
        p = Process(target=do_work_group, args=(in_queue, results_list))
        p.start()
        pool.append(p)

    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')

        group = []
        for line in csv_file:
            group.append(line)
            if len(group) >= 1000:
                in_queue.put((amount_eur_index, group))
                group = []

        if len(group) != 0:
            in_queue.put((amount_eur_index, group))
        for i in range(num_workers):
            in_queue.put((None, None))

    for p in pool:
        p.join()

    return '{:.2f}'.format(math.fsum(results_list))


def sum_multiprocess_group_100(file_name):
    num_workers = 2
    pool = []
    manager = Manager()
    results_list = manager.list()
    in_queue = Queue()
    for i in range(num_workers):
        p = Process(target=do_work_group, args=(in_queue, results_list))
        p.start()
        pool.append(p)

    with open(file_name) as csv_file:
        headers = next(csv_file).strip().split(',')
        amount_eur_index = headers.index('amount EUR')

        group = []
        for line in csv_file:
            group.append(line)
            if len(group) >= 1000:
                in_queue.put((amount_eur_index, group))
                group = []

        if len(group) != 0:
            in_queue.put((amount_eur_index, group))
        for i in range(num_workers):
            in_queue.put((None, None))

    for p in pool:
        p.join()

    return '{:.2f}'.format(math.fsum(results_list))


def plot_result_times(options, files, times, save_to='times.png', title='Time Plot'):
    width = 0.75
    fig, ax = plt.subplots()

    x_labels = [file[:-4].replace('_', '') for file in files]
    x = np.arange(len(x_labels))
    for idx, times_for_option in enumerate(times):
        bars_in_group = len(times)
        bar_width = width / bars_in_group
        ax.bar(x + bar_width * idx - width/2,
               times_for_option, width=bar_width, label=options[idx].__name__)

    ax.set_ylabel('Seconds')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()
    ax.set_yscale('log')
    plt.savefig(save_to)


def plot_result_time_per_row(options, files, times, save_to='scaled_times.png', title='Scaled Time Plot'):
    width = 0.75
    fig, ax = plt.subplots()

    x_labels = [file[:-4].replace('_', '') for file in files]
    x = np.arange(len(x_labels))

    scaled_times = [[time*1000000/float(x_labels[idx]) for idx, time in enumerate(option_times)] for option_times in times]
    for idx, times_for_option in enumerate(scaled_times):
        bars_in_group = len(scaled_times)
        bar_width = width / bars_in_group
        ax.bar(x + bar_width * idx - width/2,
               times_for_option, width=bar_width, label=options[idx].__name__)

    ax.set_ylabel('Nanoseconds')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.savefig(save_to)


def time_algorithms():
    folder = '../test_files/'
    files = ['1000.csv', '10_000.csv', '100_000.csv', '1_000_000.csv', '10_000_000.csv', '100_000_000.csv']
    expected_sums = ['4800.76', '48007.60', '480076.00', '4800760.00', '48007600.00', '480076000.00']

    file_reading_options = [read_file, read_file_csv, read_file_split, read_file_pandas]
    file_sum_options = [sum_csv_int, sum_csv_int_comprehension, sum_csv_fsum, sum_csv_decimal,
                        sum_split_int, sum_split_int_comprehension, sum_split_fsum, sum_split_decimal, sum_pandas,
                        sum_dask_pandas, sum_multiprocess_group_1000, sum_multiprocess_group_100]

    ###
    # Run and time reading options
    ###
    reading_result_times = []
    for option in file_reading_options:
        print(f'Timing reading option "{option.__name__}"')
        reading_option_times = []
        for idx, file in enumerate(files):
            start = time.time()
            option(f'{folder}{file}')
            end = time.time()
            reading_option_times.append(end-start)
            
        reading_result_times.append(reading_option_times)

    print('Done timing reading options')
    print(reading_result_times)

    '''
    # times used to generate charts in repo
    reading_result_times = [
        [0.0027282238006591797, 0.003737211227416992, 0.019328832626342773, 0.13662481307983398, 1.3230268955230713, 12.718315839767456],
        [0.0010440349578857422, 0.00943899154663086, 0.08784317970275879, 0.8659260272979736, 8.933452129364014, 86.89902019500732],
        [0.0006568431854248047, 0.005713224411010742, 0.06008100509643555, 0.5573468208312988, 5.665111064910889, 56.4782280921936],
        [0.005586862564086914, 0.007875919342041016, 0.06015205383300781, 0.47529006004333496, 4.957808017730713, 63.14728498458862]
    ]
    '''

    plot_result_times(file_reading_options, files, reading_result_times, save_to='reading_times.png',
                      title='Clock Time Reading Files')
    plot_result_time_per_row(file_reading_options, files, reading_result_times, save_to='reading_times_per_row.png',
                             title='Clock Time Reading Files Per Row')

    ###
    # Run and time summing options
    ###
    sum_result_times = []
    for option in file_sum_options:
        print(f'Timing sum option "{option.__name__}"')
        sum_option_times = []
        for idx, file in enumerate(files):
            start = time.time()
            total = option(f'{folder}{file}')
            if total != expected_sums[idx]:
                print(f'{option.__name__} failed to sum file {file} correctly. Got result {total}. Setting time to zero.')
                sum_option_times.append(0)
                continue
            end = time.time()
            sum_option_times.append(end-start)

        sum_result_times.append(sum_option_times)

    print('Done timing sums')
    print(sum_result_times)

    '''
    # times used to generate charts in repo
    sum_result_times = [
        [0.03610396385192871, 0.023204803466796875, 0.1529839038848877, 1.4663259983062744, 12.929994821548462, 129.0347831249237],
        [0.0013382434844970703, 0.012452840805053711, 0.1243891716003418, 1.2713370323181152, 12.774251937866211, 128.68864798545837],
        [0.0014913082122802734, 0.011362791061401367, 0.1121828556060791, 1.0520739555358887, 10.963155031204224, 109.81400322914124],
        [0.001516103744506836, 0.012539863586425781, 0.11394190788269043, 1.2496697902679443, 12.412419080734253, 148.2140941619873],
        [0.004858970642089844, 0.0121002197265625, 0.09480929374694824, 0.9635820388793945, 9.68176007270813, 95.5725667476654],
        [0.0015518665313720703, 0.013486146926879883, 0.14008092880249023, 1.3432776927947998, 13.687088251113892, 137.869304895401],
        [0.001194000244140625, 0.008501052856445312, 0.07723402976989746, 0.7829320430755615, 7.894617080688477, 79.75020480155945],
        [0.0012021064758300781, 0.008955001831054688, 0.0827629566192627, 0.9249470233917236, 9.426769018173218, 120.88330912590027],
        [0.08045792579650879, 0.010688066482543945, 0.057878971099853516, 0.4840562343597412, 4.66231107711792, 49.72357201576233],
        [0.05176115036010742, 0.04227614402770996, 0.10026288032531738, 0.6557419300079346, 3.360474109649658, 29.80898904800415],
        [0.034432172775268555, 0.04058694839477539, 0.10614895820617676, 0.8746130466461182, 7.668174743652344, 113.19796800613403],
        [0.05296802520751953, 0.037930965423583984, 0.09582901000976562, 0.7705349922180176, 9.90707278251648, 110.95649099349976],
    ]
    '''

    plot_result_times(file_sum_options, files, sum_result_times, save_to='sum_times.png',
                      title='Clock Time Summing Files')
    plot_result_time_per_row(file_sum_options, files, sum_result_times, save_to='sum_times_per_row.png',
                             title='Clock Time Summing Files Per Row')
    plot_result_time_per_row(file_sum_options, files[1:],
                             [result_times[1:] for result_times in sum_result_times],
                             save_to='sum_times_per_row_no_1000.png',
                             title='Clock Time Summing Files Per Row (No 1000)')

if __name__ == "__main__":
    time_algorithms()
