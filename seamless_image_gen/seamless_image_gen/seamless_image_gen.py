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
    @staticmethod
    def proc(image: np.ndarray) -> np.ndarray:
        center_x = image.shape[1] / 2
        center_y = image.shape[0] / 2

        image_2x1 = np.concatenate((image, image), axis=0)
        image_2x2 = np.concatenate((image_2x1, image_2x1), axis=1)
        return image_2x2[
            int(center_y) : int(center_y + image.shape[1]),
            int(center_x) : int(center_x + image.shape[0]),
        ]


class CenterCrossMaskImageGenerator(CV2IdenticalImageGenerator):
    @staticmethod
    def proc(image: np.ndarray) -> np.ndarray:
        mask = np.zeros(image.shape[:2], dtype="uint8")
        center_x = mask.shape[1] / 2
        center_y = mask.shape[0] / 2
        w = mask.shape[1] * 0.1
        h = mask.shape[0] * 0.1
        x = center_x - w / 2
        y = center_y - h / 2
        mask[int(y) : int(y + h), :] = 1
        mask[:, int(x) : int(x + w)] = 1
        mask = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2RGB)
        return mask
