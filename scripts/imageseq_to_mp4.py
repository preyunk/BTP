import cv2
import glob
img_array = []
for filename in sorted(glob.glob('UAV123_10fps/data_seq/UAV123_10fps/car5/*.jpg')):
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    print(size)
    img_array.append(img)


out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'XVID'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()