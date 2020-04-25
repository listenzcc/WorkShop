# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
""" Basic setting """
VAL_NUM = 30
VAL_LIMITS = (1, 10)
IMG_SIZE = (800, 600)
IMG_AREA = np.prod(IMG_SIZE)

VAL_NUM, VAL_LIMITS, IMG_SIZE

# %%
""" Init random frame """
FRAME = pd.DataFrame(columns=['name', 'size', 'area', 'start', 'end', 'check'])
for j in range(VAL_NUM):
    size = np.random.randint(low=VAL_LIMITS[0], high=VAL_LIMITS[1])
    FRAME = FRAME.append(pd.Series(dict(
        name=f'Node {j}',
        size=size,
    )), ignore_index=True)

area = FRAME['size'].sum()
FRAME['area'] = FRAME['size'] / area * IMG_AREA

FRAME = FRAME.sort_values(by='size', ascending=False)
FRAME

# %%


def best_stack(top_idx, depth, FRAME=FRAME):
    num = 0
    last_diff = np.inf

    for _ in range(len(FRAME)):
        num += 1
        area = FRAME.iloc[top_idx: top_idx + num]['area'].sum()
        width = area / depth
        diff = abs(width - FRAME.iloc[top_idx]['area'] / width)
        if diff > last_diff:
            num -= 1
            break
        last_diff = diff

    area = FRAME.iloc[top_idx: top_idx + num]['area'].sum()
    width = area / depth

    return num, width, area


start = (0, 0)
top_idx = 0
# num = 0
# width = 0
# FRAME.iloc[0]['start'] = start

for _ in range(10):
    # 0 Session
    try:
        depth = IMG_SIZE[0] - start[0]
        num, width, area = best_stack(top_idx, depth)
        for j in range(top_idx, top_idx + num):
            FRAME.iloc[j]['start'] = tuple(start)
            _depth = depth / area * FRAME.iloc[j]['area']
            FRAME.iloc[j]['end'] = (start[0] + _depth, start[1] + width)
            start = (start[0] + _depth, start[1])

        start = (FRAME.iloc[top_idx]['start'][0], start[1] + width)
        top_idx += num
    except:
        break

    # 1 Session
    try:
        depth = IMG_SIZE[1] - start[1]
        num, width, area = best_stack(top_idx, depth)
        for j in range(top_idx, top_idx + num):
            FRAME.iloc[j]['start'] = tuple(start)
            _depth = depth / area * FRAME.iloc[j]['area']
            FRAME.iloc[j]['end'] = (start[0] + width, start[1] + _depth)
            start = (start[0], start[1] + _depth)

        start = (start[0] + width, FRAME.iloc[top_idx]['start'][1])
        top_idx += num
    except:
        break

FRAME

# %%


def draw(FRAME=FRAME, IMG_SIZE=IMG_SIZE):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for j in range(len(FRAME)):
        series = FRAME.iloc[j]
        if not pd.isna(series['start']):
            start, end = series[['start', 'end']]
            size = (end[0] - start[0], end[1] - start[1])
            FRAME.iloc[j]['check'] = np.prod(size)
            rect = plt.Rectangle(start,
                                 size[0], size[1],
                                 linewidth=3, edgecolor='k', fill=False)
            ax.add_patch(rect)

    ax.set_xlim(0, IMG_SIZE[0])
    ax.set_ylim(0, IMG_SIZE[1])
    return fig


fig = draw()
plt.show()

FRAME
# %%

# %%
