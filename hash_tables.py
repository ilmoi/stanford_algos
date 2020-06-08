# didn't realize this, but dicsts are actually implemented as hash tables underneath
# this explains why you can't have a mutable object as a key
# the key needs to be hashable and mutable python objects (lists, dicts) are not
# python's dicts are optimized and provide O(1) performance for lookup, insert, update, delete, on average

# some other implementations of dicts that ship in standard library:
# this one remembers order of key insertion
# (although in CPython implementation 3.6+ that's done for normal dicts too)

import collections
d = collections.OrderedDict(one=1, two=2, three=3)
print(d)
d['four'] = 4
print(d)
print(d.keys())


# this implementation supports a default value that is returned in case key not found
from collections import defaultdict
dd = defaultdict(list) #in this case default struct is a list
print(dd)
print(dd['dogs']) #returns empty list
dd['dogs'].append('rufus')
print(dd)
print(dd['dogs'])

# this implementation groups multiple dictionaries into a single mapping
from collections import ChainMap
dict1 = {'one': 1, 'two': 2}
dict2 = {'three': 3, 'four': 4}
chain = ChainMap(dict1, dict2)
print(chain)
print(chain['one'])
print(chain['three'])
# I think it's the same effect as this:
dict3 = {**dict1, **dict2}
print(dict3)

# this implementation allows to create immutable dicts by wrapping them
from types import MappingProxyType
read_only = MappingProxyType({'one':1, 'two':2})
print(read_only['one'])
read_only['one'] = 24 #TypeError - does not support assignment

