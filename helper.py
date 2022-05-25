import numpy as np
from PIL import Image
import requests
from io import BytesIO

def random_colors(num_of_color, img):
    num_channel = img.shape[2]
    if num_channel != 3 and num_channel != 4:
        raise Exception("Image must has at least three channels.")
    flat_img = img.reshape((-1, num_channel))
    idx = (np.random.rand(1, num_of_color) * flat_img.shape[0]).astype(int)
    colors = np.array([flat_img[i] for i in idx])[0]
    return colors

def random_pivots(num_of_band: int):
    random_n2 = np.random.rand(num_of_band-1,2)
    return np.sort(random_n2)

def sorted_pivots_by_width(pivots):
    working_pivots = pivots.T # nx2 for calculating the width 
    width = np.array(working_pivots[1]-working_pivots[0])  # nx1
    width_reshape = np.reshape(width, (1, len(width))) #[nx1]
    working_pivots = np.concatenate((working_pivots, width_reshape)).T # nx3 -> 3xn
    sorted_indexes = working_pivots[:, 2].argsort() 
    return pivots[sorted_indexes] # sort by width and make to paint the big one first

def get_sorted_pivots(num_of_band):
    pivots = random_pivots(num_of_band)
    return sorted_pivots_by_width(pivots).tolist()

def get_img_colors(image_path, num_colors):
    im = Image.open(image_path)
    data = np.asarray(im)
    return random_colors(num_colors, data)

def img_from_url(url):
    response = requests.get(url)
    img_path=BytesIO(response.content)
    return img_path
