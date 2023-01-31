import os
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = os.path.dirname(__file__)
this_root = os.path.dirname(this_dir)
# print('Module    sys.path  ==> ', sys.path)
add_path(os.path.join(this_root, 'src'))


from gy_redis import RedisManager
print('12312', RedisManager)