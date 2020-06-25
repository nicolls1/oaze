# This file loads the django environment for use from dask
# Use 'dask-worker --preload /path/to/this/file/daskwokerinit.py <scheduler_address>'
# to have django environment on a worker

import django
print('starting worker setup...')

django.setup()

print('worker setup finished!')
