import dask.dataframe as dd


def sum_csv(file_name):
    df = dd.read_csv(file_name)
    return {
        'sum': '{:.2f}'.format(df['amount EUR'].sum().compute()),
        'lines': df.shape[0].compute(),
    }
