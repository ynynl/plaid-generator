# %%
import matplotlib.pyplot as plt

import numpy as np

from PIL import Image

from numpy.core.records import array

from io import BytesIO
import base64


# %%

# Generate random colors
def random_rbg(num_colors, intensity_range, random):
    colors = [random.randint(r[0], r[1]+1, size=num_colors)
              for r in intensity_range]
    return np.transpose(colors)


def grid(l):
    edge_size = l.shape[0]
    row, col = np.ogrid[:edge_size, :edge_size]
    mask = np.isin((row % 4 + col % 4), [3, 4, 0])
    v = np.tile(l, (l.shape[1], 1, 1))
    v[mask] = np.rot90(v)[mask]
    return v


def show(img, repeat_row, repeat_col):
    f = np.tile(img, (repeat_col, repeat_row, 1))
    # pad_arr = np.pad(tartan, ((128,128), (128,128), (0, 0)), 'wrap')
    plt.figure()
    plt.imshow(f)
    plt.axis('off')
    plt.show()


# initialize a line as the base
def line(size, color):
    l = np.zeros((1, size, 3)).astype(int)
    l[0, :] = color[:3]
    return l

# Add a band to the line


def add_band(l, color, mark):
    # Transfer the float arrary into two int numbers
    r = ((l.shape[1]-1) * mark).astype(int)
    l[:, r[0]:r[1]] = color[:3]
    return l

# colors: 3 by n or 4 by n ndarray that stores list of RGB colors.
# edge_size: must be mutiple of 4.


def random_tartan(colors, edge_size=128,  twill='tartan', random_seed=None):
    # Generate a line as edge.
    # Use the first array as background

    assert (edge_size % 8 == 0), "Edge size must be multiples of four."
    l = line(edge_size, colors[0])
    num_color = colors.shape[0]
    random = np.random.RandomState(random_seed)

    # Generate a band by two random points on the baseline:
    marks = random.rand(num_color-1, 2)  # n x 2
    marks = np.sort(marks)
    mT = marks.T  # 2xn
    width = np.array(mT[1]-mT[0])  # 1xn
    width = np.reshape(width, (1, len(marks)))
    m = np.concatenate((mT, width)).T
    marks = m[m[:, 2].argsort()]

    # print(marks)
    for i in range(num_color-2, -1, -1):
        l = add_band(l, colors[i+1], marks[i])

    # Expand the line into a square image:
    # edge_size = l.shape[1]
    # pad_size = int(0.5*(edge_size-4))
    v = np.tile(l, (edge_size, 1, 1))

    # Create a pattern mask:

    dict = {
        'tartan': np.array([
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 0]
        ]).astype('bool'),

        'madras': np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]).astype('bool'),

        # 3: np.array([
        #             [0,0,1,1,0,0,0,0],
        #             [0,0,1,0,0,1,0,0],
        #             [0,0,1,1,1,1,1,1],
        #             [0,1,1,1,1,1,1,0],
        #             [1,1,1,1,1,1,0,0],
        #             [1,0,1,1,1,1,0,1],
        #             [0,0,0,0,1,1,0,0],
        #             [0,0,0,1,1,0,0,0]
        #             ]).astype('bool'),

        'net': np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1]
        ]).astype('bool'),

    }

    t = dict[twill]

    num_tile = int(edge_size/t.shape[0])

    # pad_arr = np.pad(t, (pad_size+edge_size%2,pad_size), 'wrap')
    mask = np.tile(t, (num_tile, num_tile))

    # Apply mask:
    v[mask] = np.rot90(v)[mask]

    return v


def pick(num_color, img):
    num_channel = img.shape[2]
    if num_channel != 3 and num_channel != 4:
        raise Exception("Image must has at least three channels.")

    flat_img = img.reshape((-1, num_channel))
    idx = (np.random.rand(1, num_color) * flat_img.shape[0]).astype(int)

    picks = np.array([flat_img[i]
                      for i in idx])[0]
    return picks


def img_to_tartan(image_path, num_colors, edge_size=128, display=False):
    im = Image.open(image_path)
    data = np.asarray(im)

    colors = pick(num_colors, data)
    tartan = random_tartan(colors, edge_size)
    if display:
        show(tartan, 2, 1)
    return tartan


def rgbTotartan(colors, size, twill):
    colors = np.array(colors)
    array = random_tartan(colors, size, twill)
    image = Image.fromarray(np.uint8(array))
    buffered = BytesIO()
    image.save(buffered, format="png")
    # print(type(buffered))
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return "data:image/  png;base64," + img_str
# %%
