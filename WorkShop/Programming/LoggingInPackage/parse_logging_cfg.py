# File: parse_logging_cfg.py
# Aim: Parse the logging cfg file, and visualize it.

# %%
import os
import pandas as pd


class CfgObject(object):
    # Object of cfg file
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.DataFrame()

    def get_cards(self):
        with open(self.filename, 'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break

                if len(line) < 2:
                    continue

                self._parse_line(line)

    def _parse_line(self, line):
        print('-', line)

        if line.startswith('['):
            contents = line[1:-2].split('_')
            if len(contents) == 2:
                self.CLASS, self.NAME = contents
                return
            if len(contents) == 1:
                self.CLASS, self.NAME = 'register', contents[0]
                return
            return

        key, value = line.split('=', 2)
        value = value[:-1]
        se = pd.Series(dict(CLASS=self.CLASS,
                            NAME=self.NAME,
                            key=key,
                            value=value))
        self.df = self.df.append(se, ignore_index=True)


filename = os.path.join('somePackage', 'logging.cfg')
cfg = CfgObject(filename)
cfg.get_cards()
cfg.df
# %%
