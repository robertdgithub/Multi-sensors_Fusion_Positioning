# -*- coding: utf-8 -*-
from IPython.core.display import HTML
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import json
import numpy as np
import sys
from contextlib import contextmanager


def equal_axis():
    pylab.rcParams['figure.figsize'] = 10,10
    plt.axis('equal')

def reset_axis():
    pylab.rcParams['figure.figsize'] = 11, 5.5

def set_figsize(x, y):
    pylab.rcParams['figure.figsize'] = x, y


@contextmanager
def figsize(x,y):
    """Temporarily set the figure size using 'with figsize(a,b):'"""

    set_figsize(x,y)
    yield
    reset_axis()

@contextmanager
def numpy_precision(precision):
	old = np.get_printoptions()['precision']
	np.set_printoptions(precision=precision)
	yield
	np.set_printoptions(old)
	
	
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def load_style(directory = '.', name='/custom2.css'):
    if sys.version_info[0] >= 3:
        s = json.load(open(directory + "/538.json"))
    else:
        s = json.load(open(directory + "/538.json"), object_hook=_decode_dict)
    plt.rcParams.update(s)
    reset_axis ()
    np.set_printoptions(suppress=True)

    styles = open(directory + name, 'r').read()
    return HTML(styles)
