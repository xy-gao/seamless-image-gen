from abc import ABCMeta, abstractmethod

import cv2
import numpy as np


class ImageGenerator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def read(input_path):
        pass

    @staticmethod
    @abstractmethod
    def write(output_path, image):
        pass

    @staticmethod
    @abstractmethod
    def proc(image):
        pass

    @classmethod
    @abstractmethod
    def __call__(cls, input_path, output_path):
        cls.write(output_path, cls.proc(cls.read(input_path)))


class CV2IdenticalImageGenerator(ImageGenerator):
    @staticmethod
    def read(input_path: str) -> np.ndarray:
        return cv2.imread(input_path)

    @staticmethod
    def write(output_path: str, image: np.ndarray) -> None:
        cv2.imwrite(output_path, image)

    @staticmethod
    def proc(image: np.ndarray) -> np.ndarray:
        return image

    @classmethod
    def __call__(cls, input_path, output_path):
        return super().__call__(input_path, output_path)


class CenterOfTileImageGenerator(CV2IdenticalImageGenerator):
    pass
