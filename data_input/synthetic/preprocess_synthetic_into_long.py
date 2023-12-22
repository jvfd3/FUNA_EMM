import pandas as pd
import numpy as np
import string

def into_long(ddlong=None, extra_descriptors=None, info=None):

    ddlong_added = add_basic_descriptors_to_long(ddlong=ddlong, extra_descriptors=extra_descriptors, info=info):

    return ddlong_added, info

def add_basic_descriptors_to_long(ddlong=None, extra_descriptors=None, info=None):

    extra_descs_invar = info['extra_desc_invar']
    extra_descs_var = info['extra_desc_var']

    ddlong_added = ddlong.copy()

    return ddlong_added
