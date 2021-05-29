from abc import ABCMeta, abstractmethod

import cv2
import numpy as np


class ImageGenerator(metaclass=ABCMeta):
    @abstractmethod
    def read(self, input_path):
        pass

    @abstractmethod
    def write(self, output_path, image):
        pass

    @abstractmethod
    def proc(self, image):
        pass

    @abstractmethod
    def __call__(self, input_path, output_path):
        self.write(output_path, self.proc(self.read(input_path)))


class CV2IdenticalImageGenerator(ImageGenerator):
    def read(self, input_path: str) -> np.ndarray:
        return cv2.imread(input_path)

    def write(self, output_path: str, image: np.ndarray) -> None:
        cv2.imwrite(output_path, image)

    def proc(self, image: np.ndarray) -> np.ndarray:
        return image

    def __call__(self, input_path, output_path):
        return super().__call__(input_path, output_path)


class CenterOfTileImageGenerator(CV2IdenticalImageGenerator):
    @staticmethod
    def proc(image: np.ndarray) -> np.ndarray:
        center_x = image.shape[1] / 2
        center_y = image.shape[0] / 2

        image_2x1 = np.concatenate((image, image), axis=0)
        image_2x2 = np.concatenate((image_2x1, image_2x1), axis=1)
        im = image_2x2[
            int(center_y) : int(center_y + image.shape[0]),
            int(center_x) : int(center_x + image.shape[1]),
        ]
        return im


class CenterCrossMaskImageGenerator(CV2IdenticalImageGenerator):
    def __init__(self, width=0.1, height=0.1):
        if (0 <= width <= 1) and (0 <= height <= 1):
            self.width = width
            self.height = height
        else:
            raise ValueError("ratio out of range")

    def proc(self, image: np.ndarray) -> np.ndarray:
        mask = np.zeros(image.shape[:2], dtype="uint8")
        center_x = mask.shape[1] / 2
        center_y = mask.shape[0] / 2
        w = mask.shape[1] * self.width
        h = mask.shape[0] * self.height
        x = center_x - w / 2
        y = center_y - h / 2
        mask[int(y) : int(y + h), :] = 1
        mask[:, int(x) : int(x + w)] = 1
        mask = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2RGB)
        return mask


class ResizedImageGenerator(CV2IdenticalImageGenerator):
    def __init__(self, width=512, height=512):
        self.width = width
        self.height = height

    def proc(self, image: np.ndarray) -> np.ndarray:
        im = cv2.resize(image, (self.width, self.height))
        return im
