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

***

### *Tracking - YOLOv3 + DeepSORT*

### Check all dependencies installed
```
pip install -r requirements.txt
```

### Update configurations
Make sure to change the paths specified in `yaml` files which are basically the configuration files for the model to be used.

Create a video from UAV123 dataset image sequence which will serve as our input. The required script to convert image sequence to mp4 video could be found in scripts directory.

### Download deepsort parameters ckpt.t7
```
cd deep_sort/deep/checkpoint
# download ckpt.t7 from
https://drive.google.com/drive/folders/1xhG0kRH1EX5B9_Iz8gQJb7UNnn_riXi6 to this folder
cd ../../../
```

### Build python NMS
```
cd /content/BTP/detector/YOLOv3/nms/ext/ && python build.py build_ext develop
```

### Run demo
```
usage: deepsort.py [-h]
                   [--fastreid]
                   [--config_fastreid CONFIG_FASTREID]
                   [--mmdet]
                   [--config_mmdetection CONFIG_MMDETECTION]
                   [--config_detection CONFIG_DETECTION]
                   [--config_deepsort CONFIG_DEEPSORT] [--display]
                   [--frame_interval FRAME_INTERVAL]
                   [--display_width DISPLAY_WIDTH]
                   [--display_height DISPLAY_HEIGHT] [--save_path SAVE_PATH]
                   [--cpu] [--camera CAM]
                   VIDEO_PATH
```

Use `--display` to enable display.

Results will be saved to `./output/results.avi` and `./output/results.txt.`

***
### *Model Optimization*

### Requirements
- pytorch >= 1.0
- darknet
- ultralytics/yolov3

### IMPORTANT Instructions
1. TO run sparsity training and channel pruning, `ultralytics/yolov3` is required.

2. We only provide the pruning method for channel pruning (prune.py) and subgradient method for sparsity training (sparsity.py).

3. Sparsity training can be done by using updateBN() in sparsity.py before optimizer.step() in train.py.
4. The channel pruning can be done by prune.py.

### Sparsity Training
```
python yolov3/train.py --cfg VisDrone2019/yolov3-spp3.cfg --data-cfg VisDrone2019/drone.data -sr --s 0.0001 --alpha 1.0
```

### Channel Pruning
```
python yolov3/prune.py --cfg VisDrone2019/yolov3-spp3.cfg --data-cfg VisDrone2019/drone.data --weights yolov3-spp3_sparsity.weights --overall_ratio 0.5 --perlayer_ratio 0.1
```

### Fine Tuning
```
./darknet/darknet detector train VisDrone2019/drone.data  cfg/prune_0.5.cfg weights/prune_0.5/prune.weights
```