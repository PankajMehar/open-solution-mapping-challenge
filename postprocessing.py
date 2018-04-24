import numpy as np
from scipy import ndimage as ndi
import tqdm
from skimage.transform import resize

from steps.base import BaseTransformer


class Thresholder(BaseTransformer):
    def __init__(self, threshold):
        self.threshold = threshold

    def transform(self, images):
        binarized_images = []
        for image in images:
            binarized_image = (image > self.threshold).astype(np.uint8)
            binarized_images.append(binarized_image)
        return {'binarized_images': binarized_images}


class BuildingLabeler(BaseTransformer):
    def transform(self, images):
        labeled_images = []
        for i, image in enumerate(images):
            labeled_image = label_multichannel_image(image)
            labeled_images.append(labeled_image)

        return {'labeled_images': labeled_images}


class Resizer(BaseTransformer):
    def transform(self, images, target_sizes):
        resized_images = []
        for image, target_size in tqdm(zip(images, target_sizes)):
            resized_image = resize(image, target_size, mode='constant')
            resized_images.append(resized_image)
        return {'resized_images': resized_images}

def label(mask):
    labeled, nr_true = ndi.label(mask)
    return labeled

def label_multichannel_image(mask):
    labeled_channels = []
    for channel in mask:
        labeled_channels.append(label(channel))
    labeled_image = np.stack(labeled_channels)
    return labeled_image