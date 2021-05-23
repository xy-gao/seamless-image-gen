from abc import ABCMeta, abstractmethod

import cv2


class ImageGenerator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def proc(input_path, output_path):
        pass


class OriginalImageGenerator(ImageGenerator):
    @staticmethod
    def proc(input_path, output_path):
        cv2.imwrite(output_path, cv2.imread(input_path))
