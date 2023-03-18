import os
import cv2

downloaded_images_dir = 'YOLO-Coco-Dataset-Custom-Classes-Extractor\downloaded_images'

# loop through each class and each image
for class_name in os.listdir(downloaded_images_dir):
    class_dir = os.path.join(downloaded_images_dir, class_name)
    for subset in ['train', 'test', 'validation']:
    # for subset in ['validation']:
        subset_dir = os.path.join(class_dir, subset)
        image_dir = os.path.join(subset_dir, 'images')
        label_dir = os.path.join(subset_dir, 'labels')
        for image_file in os.listdir(image_dir):
            # load the image
            image_path = os.path.join(image_dir, image_file)
            image = cv2.imread(image_path)

            # load the corresponding label
            label_file = image_file.split('.')[0] + '.txt'
            label_path = os.path.join(label_dir, label_file)
            with open(label_path, 'r') as f:
                label = f.readline().strip().split()

            # visualize the label on the image
            x, y, w, h = map(float, label[1:])
            left = int((x - w / 2) * image.shape[1])
            top = int((y - h / 2) * image.shape[0])
            right = int((x + w / 2) * image.shape[1])
            bottom = int((y + h / 2) * image.shape[0])
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            # show the image and ask for user input
            cv2.imshow(image_file, image)
            key = cv2.waitKey(0)

            # if the label is bad, delete the label and image
            if key == ord('r'):
                os.remove(image_path)
                os.remove(label_path)
            if key == 27:
                cv2.destroyAllWindows()
                break


            cv2.destroyAllWindows()