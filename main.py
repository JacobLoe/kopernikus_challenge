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
                        help='input directory')
    parser.add_argument('--pixel_threshold', type=int, default=10e5,
                        help='input directory')

    args = parser.parse_args()

    path_to_dataset = '../dataset-candidates-ml/dataset'
    images_path = glob.glob(os.path.join(path_to_dataset, '*.png'))
    # sort images by name
    images_path = sorted(images_path)
    print('number of images', len(images_path))
    #
    # # 640 * 480
    # image0 = 'c10-1623871124416.png'
    # image1 = 'c10-1623872200494.png' # same as image0
    # image2 = 'c10-1623872544167.png' # new lighting
    # image3 = 'c10-1623898673581.png' # new lighting
    # image4 = 'c10-1623904861138.png' # natural lighting
    #
    # gg = [image0, image1, image2, image3, image4]
    #
    # print('pair, score')
    # c = []
    # for i, gi in enumerate(gg):
    #     for j, gj in enumerate(gg):
    #         img0 = cv2.imread(os.path.join(path_to_dataset, gi))
    #         img0 = preprocess_image_change_detection(img0)
    #         img1 = cv2.imread(os.path.join(path_to_dataset, gj))
    #         img1 = preprocess_image_change_detection(img1)
    #
    #         score, res_cnts, thresh = compare_frames_change_detection(img0, img1, args.min_contour_area)
    #         print((i, j), score)
    #
    # print('-------------------------')
    #
    # # 1920 * 1080
    # image0 = 'c20-1616770189783.png'
    # image1 = 'c20-1616772931032.png' # light
    # image2 = 'c20-1616773273560.png' # car
    # image3 = 'c20-1616776014667.png' # more car
    # image4 = 'c20_2021_04_27__11_47_19.png' # even more car
    #
    # gg = [image0, image1, image2, image3, image4]
    #
    # print('pair, score')
    # c = []
    # for i, gi in enumerate(gg):
    #     for j, gj in enumerate(gg):
    #         img0 = cv2.imread(os.path.join(path_to_dataset, gi))
    #         img0 = preprocess_image_change_detection(img0)
    #         img1 = cv2.imread(os.path.join(path_to_dataset, gj))
    #         img1 = preprocess_image_change_detection(img1)
    #
    #         score, res_cnts, thresh = compare_frames_change_detection(img0, img1, args.min_contour_area)
    #         print((i, j), score)

    print('\ngrouping images by resolution')
    # first pass, go through the images and group the images by resolution
    images_dict = {}
    for image0 in tqdm(images_path):
        img0 = cv2.imread(image0)

        if np.shape(img0) not in images_dict:
            images_dict[np.shape(img0)] = [image0]
        else:
            images_dict[np.shape(img0)].append(image0)

    print('resolutions images dict', images_dict.keys())
    # print(images_dict)

    # create a directory in path_to_dataset to move unwanted images
    path_to_unwanted = os.path.join(path_to_dataset, 'unwanted')
    if not os.path.exists(path_to_unwanted):
        os.mkdir(path_to_unwanted)

    print('\nsecond pass, go through the images and compare them')
    # iterate through the images
    for resolution_key in tqdm(images_dict):

        print('resolution', resolution_key)

        if resolution_key == ():
            # move unwanted images to unwanted folder
            for image in images_dict[resolution_key]:
                os.rename(image, os.path.join(path_to_unwanted, os.path.basename(image)))

            # # REMOVE IMAGES FROM DATASET
            print('remove images with resolution', resolution_key)
            # continue

        # if the total pixels of the image are lower than a certain threshold, delete it
        elif resolution_key[0] * resolution_key[1] < args.pixel_threshold:
            # move unwanted images to unwanted folder
            for image in images_dict[resolution_key]:
                os.rename(image, os.path.join(path_to_unwanted, os.path.basename(image)))

            # # REMOVE IMAGES FROM DATASET
            print('remove images with resolution', resolution_key)
            # continue

        # check whether there are enough images to compare with
        if len(images_dict[resolution_key]) > 1:
            c_dict = {}
            for i, im_path0 in tqdm(enumerate(images_dict[resolution_key]), leave=False):

                img0 = cv2.imread(im_path0)
                img0 = preprocess_image_change_detection(img0)
                c = []
                for j, im_path1 in enumerate(images_dict[resolution_key]):

                    if not i == j:
                        img1 = cv2.imread(im_path1)
                        img1 = preprocess_image_change_detection(img1)

                        score, res_cnts, thresh = compare_frames_change_detection(img0, img1, args.min_contour_area)
                        # if the score is 0 move image1 to unwanted folder
                        if score == 0:
                            os.rename(im_path1, os.path.join(path_to_unwanted, os.path.basename(im_path1)))

                    else:
                        continue

            # break
        # if there is only one image in the resolution, do nothing
        else:
            pass

    print(c_dict)