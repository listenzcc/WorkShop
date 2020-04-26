"""A DEMO of TreeMap visualization """
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
""" Basic setting """
# How many nodes
VAL_NUM = 30
# Value limits of node
VAL_LIMITS = (1, 10)
# Image size and image area
IMG_SIZE = (800, 600)
IMG_AREA = np.prod(IMG_SIZE)

VAL_NUM, VAL_LIMITS, IMG_SIZE

# %%
""" Init random frame """
# Empty frame
FRAME = pd.DataFrame(columns=['name', 'size', 'area', 'start', 'end', 'check'])
# Fill frame with [VAL_NUM] nodes
for j in range(VAL_NUM):
    size = np.random.randint(low=VAL_LIMITS[0], high=VAL_LIMITS[1])
    FRAME = FRAME.append(pd.Series(dict(
        name=f'Node {j}',
        size=size,
    )), ignore_index=True)
# Calculate 'area' column
area = FRAME['size'].sum()
FRAME['area'] = FRAME['size'] / area * IMG_AREA
# Sort frame by 'size' column
FRAME = FRAME.sort_values(by='size', ascending=False)
FRAME

# %%


def best_stack(top_idx, depth, FRAME=FRAME):
    """Calculate the best stack method,
    the aim is to make sure depth is filled,
    and **the first node** is as much as like a square.

    Arguments:
        top_idx {int} -- Top idx of FRAME used for stack calculation
        depth {float} -- The depth of the stack

    Keyword Arguments:
        FRAME {DataFrame} -- Frame of nodes (default: {FRAME})

    Returns:
        num {int} -- How many nodes to be used
        width {float} -- The width of the filled nodes
        area {float} -- The summation of the filled nodes
    """
    # Init last_diff as infinity,
    # since the aim is to find the lowest ratio between width and height
    last_diff = np.inf

    # Try from num = 0,
    # num will be no larger than length of FRAME
    num = 0
    for _ in range(len(FRAME)):
        # Try to add one more node
        num += 1
        # If no more node, break
        if top_idx + num == len(FRAME) + 1:
            break
        # Compute area summation of num nodes
        area = FRAME.iloc[top_idx: top_idx + num]['area'].sum()
        # Compute width
        width = area / depth
        # Compute ratio,
        # it is a alternative measurement of the divide,
        # it is a substitute
        diff = abs(width - FRAME.iloc[top_idx]['area'] / width)
        # If the lowest value is found, break
        if diff > last_diff:
            break
        # Record last_diff for next iteration
        last_diff = diff

    # The num is alway one more,
    # so substitute 1
    num -= 1
    # Compute area summation
    area = FRAME.iloc[top_idx: top_idx + num]['area'].sum()
    # Compute width
    width = area / depth
    # Return
    return num, width, area


""" Main loop for placing the nodes in FRAME """
# Start from original point
start = (0, 0)
# Start from the very top of the FRAME
top_idx = 0
# Loop for no more than VAL_NUM times
for _ in range(VAL_NUM):
    try:
        # 0 Session,
        # the fill direction is **first axis**
        depth = IMG_SIZE[0] - start[0]
        # Get the best stack method
        num, width, area = best_stack(top_idx, depth)
        # Stack
        for j in range(top_idx, top_idx + num):
            # Set start position
            FRAME.iloc[j]['start'] = start  # tuple(start)
            # Compute current depth
            _depth = depth / area * FRAME.iloc[j]['area']
            # Set end position
            FRAME.iloc[j]['end'] = (start[0] + _depth, start[1] + width)
            # Reset next start by adding current depth into the **first axis**
            start = (start[0] + _depth, start[1])
        # Replace the start point,
        # with the **second axis** plus width
        start = (FRAME.iloc[top_idx]['start'][0], start[1] + width)
        top_idx += num

        # 1 Session
        # the fill direction is **second axis**
        depth = IMG_SIZE[1] - start[1]
        # Get the best stack method
        num, width, area = best_stack(top_idx, depth)
        # Stack
        for j in range(top_idx, top_idx + num):
            # Set start and end position
            FRAME.iloc[j]['start'] = start  # tuple(start)
            # Compute current depth
            _depth = depth / area * FRAME.iloc[j]['area']
            # Set end position
            FRAME.iloc[j]['end'] = (start[0] + width, start[1] + _depth)
            # Reset next start by adding current depth into the **second axis**
            start = (start[0], start[1] + _depth)
        # Replace the start point,
        # with the **first axis** plus width
        start = (start[0] + width, FRAME.iloc[top_idx]['start'][1])
        top_idx += num
    except:
        # When FRAME.iloc colling is inevitable failed,
        # it will end-up to here,
        # which means the iteration is done
        break

FRAME

# %%


def draw(FRAME=FRAME, IMG_SIZE=IMG_SIZE):
    """Draw the nodes in FRAME

    Keyword Arguments:
        FRAME {DataFrame} -- The FRAME of nodes (default: {FRAME})
        IMG_SIZE {tuple} -- The image size (default: {IMG_SIZE})

    Returns:
        fig {Figure} -- The figure object
    """
    # Init figure and ax
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Draw nodes in FRAME
    for j in range(len(FRAME)):
        # Get a node
        series = FRAME.iloc[j]
        # If it has no position, ignore it
        if pd.isna(series['start']):
            continue
        # Prepare parameters
        start, end = series[['start', 'end']]
        size = (end[0] - start[0], end[1] - start[1])
        # Set 'check' column for latter check
        FRAME.iloc[j]['check'] = np.prod(size)
        # Draw the node as a rectangle
        rect = plt.Rectangle(start,
                             size[0], size[1],
                             linewidth=3, edgecolor='k', fill=False)
        # Add the rectangle into [ax]
        ax.add_patch(rect)

    # Set padding parameter
    padding = 10
    # Re scale [ax]
    ax.set_xlim(0 - padding, IMG_SIZE[0] + padding)
    ax.set_ylim(0 - padding, IMG_SIZE[1] + padding)
    # Return
    return fig


# Draw the FRAME and show it
fig = draw()
plt.show()

FRAME
# %%
