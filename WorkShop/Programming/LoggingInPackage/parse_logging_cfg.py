# File: parse_logging_cfg.py
# Aim: Parse the logging cfg file, and visualize it.

# %%
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd

# Table of nouns,
# used for detection and convertion from plural to single mode
nouns_table = dict(
    loggers='logger',
    keys='key',
    handlers='handler',
    formatters='formatter',
)


class NounConverter(object):
    # Noun converter
    def __init__(self, table=nouns_table):
        self.table = table

    def is_plural(self, word):
        # Detect if the [word] is plural
        return word in self.table

    def convert(self, word):
        # Detect and convert plural [word] into single mode
        if word not in self.table:
            # Not a plural noun,
            return word
        else:
            # Is a plural noun,
            return self.table[word]


class CfgObject(object):
    # Object of cfg file
    def __init__(self, filename, nc=NounConverter()):
        self.filename = filename
        self.nc = nc
        self.df = pd.DataFrame()

    def display(self):
        # Display the dataframe
        try:
            display(self.df)
        except NameError:
            print(self.df)

    def select(self, column, value):
        # Select rows by [value] in [column]
        return self.df.query(f'{column}=="{value}"')

    def load_file(self):
        # Read every line of the file,
        # parse them into pandas object
        with open(self.filename, 'r') as f:
            while True:
                # Read line
                line = f.readline()
                # Escape at the end of the file
                if len(line) == 0:
                    break
                # Strip the line
                line = line.strip()
                # Ignore empty line
                if len(line) == 0:
                    continue
                # Ignore comments line
                if line.startswith('#'):
                    continue
                # Parse the stripped line
                self._parse_line(line)

    def _parse_line(self, line):
        # print('-', line)
        # Parse name at name line
        if line.startswith('['):
            # Parse segment name
            contents = line[1:-1].split('_')
            if len(contents) == 2:
                # Name in two sections
                self.CLASS, self.NAME = contents
                return
            if len(contents) == 1:
                # Name in one section
                self.CLASS, self.NAME = 'register', contents[0]
                return
            return

        # Parse contents at values line
        key, value = line.split('=', 2)
        # Parse key and values
        if self.nc.is_plural(key):
            # The key with multile values
            key = self.nc.convert(key)
            for v in value.split(','):
                se = pd.Series(dict(CLASS=self.CLASS,
                                    NAME=self.nc.convert(self.NAME),
                                    KEY=key,
                                    VALUE=v))
                self.df = self.df.append(se, ignore_index=True)
        else:
            # The key with single value
            se = pd.Series(dict(CLASS=self.CLASS,
                                NAME=self.nc.convert(self.NAME),
                                KEY=key,
                                VALUE=value))
            self.df = self.df.append(se, ignore_index=True)

        # Reorder the columns
        self.df = self.df[['CLASS', 'NAME', 'KEY', 'VALUE']]


# %%
filename = os.path.join('somePackage', 'logging.cfg')
cfg = CfgObject(filename)
cfg.load_file()
cfg.display()

# %%
df = cfg.select('CLASS', 'register')
df['y'] = range(len(df))
df['size'] = 20
display(df)
fig = px.scatter(df, x='NAME', y='y', size='size', color='NAME',
                 hover_name='VALUE', text='VALUE')
fig.add_traces(go.Scatter(x=['loggers', 'handlers'], y=[2, 5]))
fig.show()

# %%
