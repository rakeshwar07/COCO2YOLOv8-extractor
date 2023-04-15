# Part 1
# yolo_coco_class_extractor

- Download  **Coco Dataset** for custrom object detection re-training.
- Multiple classes can be downloaded into different folders.

## Packages Required
1.pycocotools (pip install pycocotools==2.0.6)
2.random (comes default with python)
3.os (comes default with python)
4.requests (comes default with python)

## Usage
### 1. Clone this repository:  
`git clone https://github.com/rakeshwar07/COCO2YOLOv8-extractor.git`
### 2. Download the `[2017 Train/Val annotations \[241MB\]]` from this link `https://cocodataset.org/#download` zip file and put the *instances_train2017.json* file in the cloned repository's main directory.
### 3. See the various classes available:  
`coco_classes.txt`
### 4. Download a specific class:  
`python yolo_coco_class_extractor.py --class_name car --new_class_id 2 --num_images 50` #Download images containing class 'car' and will be labeled as class_id 2, 50 samples will be downloaded and placed in train,test and validation folder. By default 80% will go to train, 5% to test and 15% to valid
`!python yolo_coco_class_extractor.py --class_name car --new_class_id 2 --num_images 50` #For colab or jupyter notebook
### 5. Download multiple classes:  
`python yolo_coco_class_extractor.py --class_name [car,person,banana] --new_class_id [2,0,1] --num_images 100`
### Folder structure after image and label download:

```
dwn_img_labels/
└── class_name/
    ├── train/
    │   ├── images/
    │   └── labels/
    ├── test/
    │   ├── images/
    │   └── labels/
    └── validation/
        ├── images/
        └── labels/
```

# visual interpretor
-Since the annotated images may contain some mislabeled boxes or wrong classes. Therefore to remove these images we need a visual interpretor and this program does that.

## Packages required
1.opencv-python (If you are first time installer of opencv then install cmake,pillow and then opencv-python)

## Usage
Run `visual_interpretor.py`
press `r` key to remove an image along with its annotation if you feel the labeling is inaccurate else press spacebar or any key to review the next image.

# Part 2
# Visual QC to select images that have the correct bounding box in YOLO format itself
In the previous part the code to convert json format annotations into YOLO format. Here after that conversion, the images and labels created can be iterated to check its quality and remove if the bounding boxes are not rendered properly. In addition, the class name can be changed and saved to a new class name on the go.

run "Visual_QC_YOLO_dataset_part_2.ipynb"

Use spacebar to accept a label and any other button to move to the next. Finally the output will be displayed like this:

```
public_data_dummy/
└── train/
    ├── images/
    ├── labels/
```