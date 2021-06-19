import argparse
import glob
import os

import numpy as np
from imageio import imsave

from utils.dataset_processing.image import DepthImage

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate depth images from Cornell PCD files.')
    #parser.add_argument('path', type=str, help='Path to Cornell Grasping Dataset')
    args = parser.parse_args()

    pcd = '/content/drive/MyDrive/cornell_grasp_dataset/02/pcd0223.txt'
    di = DepthImage.from_pcd(pcd, (480, 640))
    di.inpaint()
    of_name = '../pcd0223test.tiff'
    print(of_name)
    imsave(of_name, di.img.astype(np.float32))