from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import os
import glob
import cv2
import numpy as np

if __name__ == "__main__":

    path_to_dataset = '../dataset-candidates-ml/dataset'
    images_path = glob.glob(os.path.join(path_to_dataset, '*.png'))
    # sort images by name
    images_path = sorted(images_path)
    # print(images_path[:10])
    print(len(images_path))

    resolution = []



    # first pass, go through the images and throw away the ones that are too small
    # the rest is saved in a dict with the resolution as key and the images as value
    images_dict = {}
    for i, image0 in enumerate(images_path):
        img0 = cv2.imread(image0)

        # compare only images with the same resolution
        # skip resolutions which contain only one image (the first image is
        if i == 0 \
                or np.shape(img0) == (6, 10, 3) \
                or np.shape(img0) == (619, 1100, 3) \
                or np.shape(img0) == (675, 1200, 3) \
                or np.shape(img0) == ():
            print('skipping image')
            if resolution != np.shape(img0):
                resolution = np.shape(img0)
        else:
            
            if resolution != np.shape(img0):
                print(i, np.shape(img0))
                resolution = np.shape(img0)


        # # print('img type, np.shape', type(img0), np.shape(img0))
        # # preprocess image
        # img0 = preprocess_image_change_detection(img0)
        # # print('preprocessed img type, np.shape', type(img0), np.shape(img0), '\n')
        # for image1 in images_path[:20]:
        #     img1 = cv2.imread(image1)
        #     img1 = preprocess_image_change_detection(img1)
        #     print('img0 type, np.shape', type(img0), np.shape(img0))
        #     print('img1 type, np.shape', type(img1), np.shape(img1))
        #     compare_frames_change_detection(img0, img1, min_contour_area=1000)
        #     print('\n')

        # break
