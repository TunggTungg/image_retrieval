from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from utils import load_image
import numpy as np
class FeatureExtractor: # TensorRT Model
    def __init__(self, mode='trt'):
        self.mode = mode
        if self.mode == 'trt':
            self.model = tf.saved_model.load('model', tags=[tag_constants.SERVING])
            self.infer = self.model.signatures['serving_default']
        else: self.model = ResNet50(weights="weight_resnet50.h5", include_top=False, pooling='avg')

    def extract(self, path):
        input_image = load_image(path)
        x = preprocess_input(input_image)  # Subtracting avg values for each pixel  
        if self.mode == 'trt':
            x = tf.constant(x, dtype=tf.float32)
            feature = self.infer(x)['avg_pool'].numpy()
        else: feature = self.model.predict(x)  # (1, 2048)
        return feature # Normalize

if __name__ == '__main__':
    fe = FeatureExtractor()
    arr = fe.extract('test.jpg')[0]
    print(arr)
    print(np.max(arr))
    print(np.min(arr))
