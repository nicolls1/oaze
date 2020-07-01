from unittest import TestCase

from dask.distributed import Client

from graphs.graphs import sum_csv_graph

client = Client(n_workers=2, threads_per_worker=1, memory_limit='1GB')


class SumCsvGraphTests(TestCase):
    csv_path = 'testfiles/1000.csv'
    csv_no_eur_path = 'testfiles/30_no_eur.csv'
    csv_no_file = 'testfiles/DOES NOT EXIST.csv'

    def test_working_file(self):
        delayed = sum_csv_graph(self.csv_path)
        future = client.compute(delayed)
        result = future.result()
        self.assertEqual(result['sum'], '4800.76')
        self.assertEqual(result['lines'], 1000)

    def test_no_eur_column(self):
        delayed = sum_csv_graph(self.csv_no_eur_path)
        with self.assertRaises(KeyError):
            future = client.compute(delayed)
            future.result()

    def test_no_file(self):
        delayed = sum_csv_graph(self.csv_no_file)
        with self.assertRaises(FileNotFoundError):
            future = client.compute(delayed)
            future.result()
