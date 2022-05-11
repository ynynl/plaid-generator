# %%
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from PIL import Image
from io import BytesIO
import base64
import math

class Plaid:
    def __init__(self, colors: list, pivots: list, size: int, twill: str):
        assert (size % 4 == 0), "Tartan size must be multiples of four."
        assert (len(colors) == len(pivots)+1), "num of colors must be one more than the num of pivots (background)."
        self.colors = np.array(colors)
        self.pivots = np.array(pivots)
        self.size = size
        self.twill = twill
        self.array = self.generate()

    __patterns = {
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

        'net': np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1]
        ]).astype('bool'),
    }

    def generate(self) -> npt.NDArray:
        warp = self.__get_warp()
        array = self.__apply_twill(warp)
        return array

    def get_png(self, width: int=None, height: int=None) -> str:
        if not width:
            width = self.size
        if not height:
            height = self.size
        resized = self.__resize(width, height)
        image = Image.fromarray(np.uint8(resized))
        buffered = BytesIO()
        image.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return "data:image/  png;base64," + img_str

    def show(self, width: int=None, height: int=None) -> None:
        if not width:
            width = self.size
        if not height:
            height = self.size
        resized = self.__resize(width, height)
        plt.figure()
        plt.imshow(resized)
        plt.axis('off')
        plt.show()

    def __resize(self, width: int, height:int) -> npt.NDArray:
        col = math.ceil(width / self.size)
        row = math.ceil(height / self.size)
        resized = np.tile(self.array, (col, row, 1))
        resized = np.delete(resized, np.s_[height:], axis = 0)
        resized = np.delete(resized, np.s_[width:], axis = 1)
        return resized

    def __get_warp(self) -> npt.NDArray:
        num_of_band = len(self.colors)
        sett = self.__get_sett(self.colors[0]) # use the first color as the background
        for i in range(num_of_band-2, -1, -1): # add bands
            threads = ((sett.shape[1]-1) * self.pivots[i]).astype(int)  # Transfer the float arrary into two int numbers
            sett[:, threads[0]:threads[1]] = self.colors[i][:3]
        return np.tile(sett, (self.size, 1, 1))

    def __apply_twill(self, wrap: npt.NDArray) -> npt.NDArray:
        tartan_size = len(wrap)
        selected_pattern = self.__patterns[self.twill]
        num_tile = int(tartan_size/selected_pattern.shape[0])
        mask = np.tile(selected_pattern, (num_tile, num_tile))
        wrap[mask] = np.rot90(wrap)[mask]
        return wrap

    def __get_sett(self, color: list) -> npt.NDArray: # get the thread patterns
        sett = np.zeros((1, self.size, 3)).astype(int)
        sett[0, :] = color[:3]
        return sett
