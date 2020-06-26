import sys

import pandas as pd
import logging

sys.path.append('..')

from modules.keepref import KeepRefs


class IterChunks(KeepRefs):
    """Class for creating link between nodes, it shares the data between them
    A port is called by iteration ie:
    for chunk in my_port:
        my_chunk_in_dataframe = chunk
        ...
    A port can either contain a chunk of a continuous signal (it means that there is only one iteration)
    or epochs (several iterations)
    To add data use set_from_df(my_df) or set(data, stamps, columns)"""
    _count = 0

    def __init__(self, is_epoched=False):
        super(IterChunks, self).__init__()
        self.clear()
        self.is_epoched = False
        self.epoching_frequency = None
        IterChunks._count += 1
        self.id = f'Port{IterChunks._count}'

    def clear(self):
        """Clear all data from _data"""
        self._data = []

    def set_parameters(self, channels, frequency, meta={}):
        """Set channels, samplingfrequency and meta data"""
        self.channels = channels
        self.frequency = frequency
        self.meta = meta

    def set_epoched(self, epoching_frequency):
        self.is_epoched = True
        self.epoching_frequency = epoching_frequency

    def set_non_epoched(self):
        self.is_epoched = False

    def set(self, rows, timestamps, columns=None):
        """Set from raw data"""
        if columns:
            self._data.append(pd.DataFrame(rows, index=timestamps, columns=columns))
        else:
            self._data.append(pd.DataFrame(rows, index=timestamps))

    def set_from_df(self, df, name=None):
        """Set from a DataFrame object"""
        if name:
            df.meta = str(name)
        self._data.append(df)

    def log_parameters(self):
        to_log = f'{self.id} {self.frequency} {self.is_epoched} {self.epoching_frequency} {self.channels}'
        logging.debug(to_log)

    def __iter__(self):
        """Define iteration"""
        self._index = 0
        return self

    def __next__(self):
        """Define iteration"""
        if self._index == len(self._data):
            raise StopIteration
        self._index += 1
        return self._data[self._index - 1]
