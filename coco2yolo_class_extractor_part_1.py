from pycocotools.coco import COCO
import requests
import os
import random
import argparse

def download_images(class_names, new_class_ids, num_images):
    # convert class_names and new_class_ids to lists if they are not already
    if not isinstance(class_names, list):
        class_names = [class_names]
    if not isinstance(new_class_ids, list):
        new_class_ids = [new_class_ids]
    downloaded_images_dir = 'dwn_img_labels'

    for class_name, new_class_id in zip(class_names, new_class_ids):
        class_dir = os.path.join(downloaded_images_dir, class_name)

        # create train, test, and validation directories
        for subset in ['train', 'test', 'validation']:
            subset_dir = os.path.join(class_dir, subset)
            os.makedirs(os.path.join(subset_dir, 'images'), exist_ok=True)
            os.makedirs(os.path.join(subset_dir, 'labels'), exist_ok=True)

        # determine the number of images for each subset
        num_train = int(num_images * 0.8)
        num_test = int(num_images * 0.05)
        num_val = num_images - num_train - num_test

        # get image IDs for the given class
        cat_ids = coco.getCatIds(catNms=[class_name])
        img_ids = coco.getImgIds(catIds=cat_ids)
        images = coco.loadImgs(img_ids)

        # randomly shuffle the images
        random.shuffle(images)

        # download the images and annotations
        for i, im in enumerate(images):
            if i >= num_images:
                break

            image_file_name = im['file_name']
            label_file_name = im['file_name'].split('.')[0] + '.txt'

            # determine which subset this image belongs to
            if i < num_train:
                subset = 'train'
            elif i < num_train + num_test:
                subset = 'test'
            else:
                subset = 'validation'

            # check if the image has already been downloaded
            image_path = os.path.join(class_dir, subset, 'images', image_file_name)
            if os.path.exists(image_path):
                print(f"{class_name}: {image_file_name} -Image and annotations already exist!")
                continue

            # download the annotations
            ann_ids = coco.getAnnIds(imgIds=im['id'], catIds=cat_ids, iscrowd=None)
            anns = coco.loadAnns(ann_ids)

            person_count = 0
            for ann in anns:
                if ann['category_id'] == cat_ids[0]:
                    person_count += 1

            # download the image and label files if the count is at least 4; change this according to your need
            if person_count >= 4:
                # download the image
                img_data = requests.get(im['coco_url']).content
                with open(image_path, 'wb') as image_handler:
                    image_handler.write(img_data)

                with open(os.path.join(class_dir, subset, 'labels', label_file_name), 'w') as label_handler:
                    for j, ann in enumerate(anns):
                        # Yolo Format: center-x center-y width height
                        x, y, w, h = ann['bbox']
                        x /= im['width']
                        y /= im['height']
                        w /= im['width']
                        h /= im['height']
                        s = f"{new_class_id} {x+w/2} {y+h/2} {w} {h}"
                        if j < len(anns) - 1:
                            s += '\n'
                        label_handler.write(s)

                print(f"{class_name}: Downloading - {image_file_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and process images for a given class.')
    parser.add_argument('--class_name', type=str, required=True, help='Name of the class to download images for.')
    parser.add_argument('--new_class_id', type=int, required=True, help='New ID to assign to the class.')
    parser.add_argument('--num_images', type=int, required=True, help='Number of images to download.')
    args = parser.parse_args()
    coco = COCO('instances_train2017.json') #in the readme file the download link has been mentioned
    download_images(args.class_name, args.new_class_id, args.num_images)