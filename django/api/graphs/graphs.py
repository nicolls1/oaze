from dask import delayed

from graphs.nodes import *


def sum_csv_graph(csv_file):
    csv_sum = delayed(sum_csv)(csv_file)
    return csv_sum
