import matplotlib
import os
cache_dir = matplotlib.get_cachedir()
# Delete .json files in that directory, then restart Python
print(cache_dir)  # find where it is