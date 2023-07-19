from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import os
import glob
import cv2
import numpy as np
from tqdm import tqdm
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Remove duplicate (or similar) images from a folder')
    parser.add_argument('--min_contour_area', type=int, default=1000,
                        help='')
    parser.add_argument('--pixel_threshold', type=int, default=10e5,
                        help='Controls the minimum size a image needs to have to not be considered for comparison')

    args = parser.parse_args()

    path_to_dataset = '../dataset-candidates-ml/dataset'
    images_path = glob.glob(os.path.join(path_to_dataset, '*.png'))
    # sort images by name
    images_path = sorted(images_path)
    print('number of images', len(images_path))

    print('\ngrouping images by resolution')
    # first pass, go through the images and group the images by camera_id and resolution
    images_dict = {}
    for image0 in tqdm(images_path):
        img0 = cv2.imread(image0)

        camera_id = os.path.split(image0)[1][0:3]

        if camera_id not in images_dict:
            images_dict[camera_id] = {}

        if np.shape(img0) not in images_dict[camera_id]:
            images_dict[camera_id][np.shape(img0)] = [image0]
        else:
            images_dict[camera_id][np.shape(img0)].append(image0)

    # use a list to remember which images are unwanted
    pictures_to_remove = []

    print('\nsecond pass, go through the images and compare them')

    # iterate through the images
    for camera_id in tqdm(images_dict):
        for resolution_key in images_dict[camera_id]:

            if resolution_key == ():
                # move unwanted images to unwanted folder
                for image in images_dict[camera_id][resolution_key]:
                    pictures_to_remove.append(image)

            # if the total pixels of the image are lower than a certain threshold, delete it
            elif resolution_key[0] * resolution_key[1] < args.pixel_threshold:
                # move unwanted images to unwanted folder
                for image in images_dict[camera_id][resolution_key]:
                    pictures_to_remove.append(image)

            # check whether there are enough images to compare with
            if len(images_dict[camera_id][resolution_key]) > 1:
                for i, im_path0 in tqdm(enumerate(images_dict[camera_id][resolution_key]), leave=False):

                    img0 = cv2.imread(im_path0)
                    img0 = preprocess_image_change_detection(img0)
                    for j, im_path1 in enumerate(images_dict[camera_id][resolution_key]):

                        if not i == j:
                            img1 = cv2.imread(im_path1)
                            img1 = preprocess_image_change_detection(img1)

                            score, res_cnts, thresh = compare_frames_change_detection(img0, img1, args.min_contour_area)
                            # if the score is 0 move image1 to unwanted folder
                            if score == 0:
                                pictures_to_remove.append(im_path1)
                        else:
                            continue

            # if there is only one image in the resolution, do nothing
            else:
                pass

    # remove duplicate paths
    pictures_to_remove = list(set(pictures_to_remove))
    print('number of images to remove', len(pictures_to_remove))
    # create a directory in path_to_dataset to move unwanted images
    path_to_unwanted = os.path.join(path_to_dataset, 'unwanted')
    if not os.path.exists(path_to_unwanted):
        os.mkdir(path_to_unwanted)

    for image in tqdm(pictures_to_remove):

        os.remove(image)
