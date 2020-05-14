# coding: utf-8
# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# %%
__doc__

# %%
# Parameters
# Fake a dataset of population and their salary,
# the aim is to draw them in pie graph

NUM = 10
popula = np.random.randint(1, 5, size=(NUM,))
salary = np.random.randint(10, 100, size=(NUM,))

popula_ratio = popula / sum(popula) * 360
salary_ratio = salary / sum(salary)
salary_ratio = salary_ratio / max(salary_ratio)

# %%
# Drawn simple pie graph,
# show population and salary in two graphs.
fig, axes = plt.subplots(1, 2)
axes[0].pie(popula, labels=popula)
axes[0].set_title('Population')
axes[1].pie(salary, labels=salary)
axes[1].set_title('Salary')

# %%
# Draw complex pie graph,
# show population and salary in one graph,
# angle range means population,
# radius means salary.
fig, ax = plt.subplots()


def label(xy, text, ax=ax):
    """Add label on [xy]

    Arguments:
        xy {tuple} -- (x, y)
        text {str} -- The content of the label

    Keyword Arguments:
        ax {axes} -- Axes to be drawn on (default: {ax})
    """
    plt.text(xy[0], xy[1]-0.05, text, ha="center",
             family='sans-serif', size=10)


def pos(r, a, d=1):
    """Compute position

    Arguments:
        r {float} -- Radius
        a {float} -- Angle in degree

    Keyword Arguments:
        d {float} -- Scale factor (default: {1})

    Returns:
        [x, y] -- The coordinate of position.
    """
    r *= d
    s = np.sin(a / 180 * np.pi)
    c = np.cos(a / 180 * np.pi)
    return [r * c, r * s]


# No high-level api can be used,
# make several pies as patches,
# and draw them seperately.
patches = []
angle = 0
for j in range(NUM):
    # Make a patch
    r = salary_ratio[j]
    angle1 = angle + popula_ratio[j]
    patch = mpatches.Wedge([0, 0],
                           salary_ratio[j],
                           angle,
                           angle1)

    # Record the patch
    patches.append(patch)

    # Label population and salary
    a = (angle + angle1) / 2
    label(pos(r, a, 1.1), salary[j])
    label(pos(r, a, 0.8), popula[j])

    # Update init angle
    angle = angle1

# Set color for each patch
colors = np.linspace(0, 1, len(patches))
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.5)
collection.set_array(np.array(colors))

# Draw
ax.add_collection(collection)
ax.set_xlim([-1.1, 1.1])
ax.set_ylim([-1.1, 1.1])
ax.set_aspect(1)

fig.tight_layout()

# %%
plt.show()
