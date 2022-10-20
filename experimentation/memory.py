import cProfile
import itertools

def regular_io(filename):
    with open(filename, mode='r', encoding='utf-8') as file_obj:
        text = file_obj.read()

import mmap

def mmap_io(filename):
    with open(filename, mode='r', encoding='utf-8') as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            text = mmap_obj.read()

def custom_takewhile(iterable):
    for x in iterable:
        yield x

def generator_explicit(filename):
    with open(filename, 'rt',  encoding="utf-8") as file:
        lines = custom_takewhile(file)
        for line in lines:
            a = 'aa'

def generator_explicit_more(filename):
    with open(filename, 'rt',  encoding="utf-8") as file:
        lines = custom_takewhile(file)
        for line in lines:
            yield line

def more_generator(filename):
    value = generator_explicit_more(filename)

    for x in value:
        aa = 'aa'

def generator_implicit(filename):
    for line in open(filename, encoding="utf-8"):
        aa = 'aa'

if __name__ == '__main__':
    filename = 'sample.txt'

    print("This is regular call")
    cProfile.run('regular_io(filename)')

    print("This is mmap")
    cProfile.run('mmap_io(filename)')

    print("This is implict generator")
    cProfile.run('generator_implicit(filename)')

    print("This is explicit generator (metaparser)")
    cProfile.run('generator_explicit(filename)')

    print("This is more explicit generator (recordparser)")
    cProfile.run('more_generator(filename)')