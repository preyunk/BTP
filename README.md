# BTP - Object Detection and Tracking using UAV

##  <font size="5"> Usage</font>

### *Training - YOLOv3*
***
### Navigate to working directory
    cd /content

### Clone Darknet
Darknet is the framework used for training YOLO

    git clone https://github.com/AlexeyAB/darknet

### Compile darknet
    %cd darknet
    sed -i 's/GPU=0/GPU=1/g' Makefile
    cat Makefile
    make

### Training the model
- Download the initial weight
- Train the model

Download initial pre-trained weights for the convolutional layers (If you have already trained and saved the weights to your Google drive, you can skip this)

```bash
get https://pjreddie.com/media/files/darknet53.conv.74
```

### Set Yolo configurations
We need to set configurations for Yolo in order to properly train. There are few settings which we need to change in the default yolov3.cfg file.

- batch
- subdivisions (if you get memory out error, increase this 16, 32 or 64)
- max_batches (it should be classes*2000)
- steps (it should be 80%, 90% of max_batches)
- classes (the number of classes which you are going to train)
- filters (the value for filters can be calculated using (classes + 5)x3 )
- Change the values below as per your requirement

```bash
sed -i 's/width=1280/width=416/g' cfg/yolov3.cfg
sed -i 's/height=1280/height=416/g' cfg/yolov3.cfg
sed -i 's/batch=1/batch=64/g' cfg/yolov3.cfg
sed -i 's/subdivisions=1/subdivisions=64/g' cfg/yolov3.cfg
sed -i 's/subdivisions=32/subdivisions=64/g' cfg/yolov3.cfg
sed -i 's/max_batches = 500200/max_batches = 10000/g' cfg/yolov3.cfg
sed -i 's/steps=400000,450000/steps=8000,9000/g' cfg/yolov3.cfg
sed -i 's/classes=80/classes=1/g' cfg/yolov3.cfg
sed -i 's/filters=255/filters=18/g' cfg/yolov3.cfg
cat cfg/yolov3.cfg
```

### Prepare dataset
Make sure to convert the VisDrone dataset to the form required by darknet for training, the required scripts can be found in the scripts directory.

Annotation files to be added in `train.txt` and `test.txt` the file should be saved in dataset root.

YOLO configuration, data mapping file and classnames could be found in config folder.


### Execute training
Navigate to darknet root directory

Run the following command to start training
```
./darknet detector train cfg/visdrone.data cfg/yolov3-visdrone.cfg darknet53.conv.74
```

### Running predictions for single image
```
./darknet detector test cfg/visdrone.data cfg/yolov3-visdrone.cfg /gdrive/MyDrive/datasets/config/yolov3-visdrone-best.weights /content/test.jpg
```

### Evaluation of the model
Points parameter is set to 0 since we are evaluating a custom dataset (other than COCO and VGG)

```
./darknet detector map cfg/visdrone.data cfg/yolov3-visdrone.cfg /gdrive/MyDrive/datasets/config/yolov3-visdrone-best.weights -points 0
```