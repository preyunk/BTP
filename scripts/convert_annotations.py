import glob
import math
anno = sorted(glob.glob("/gdrive/MyDrive/datasets/UAV123_10fps/anno/UAV123_10fps/*.txt"))
for filename in anno:
  f = open(filename, 'r')
  lines = f.readlines()
  for i, line in enumerate(lines):
    bbox = line.split(',')
    x = float(bbox[0])/1280.0
    y = float(bbox[1])/720.0
    w = float(bbox[2])/1280.0
    h = float(bbox[3])/720.0
    if math.isnan(x):
      x = 0.0
    if math.isnan(y):
      y = 0.0
    if math.isnan(w):
      w = 0.0
    if math.isnan(h):
      h = 0.0
    lines[i] = f"0 {round(x,4)} {round(y,4)} {round(w,4)} {round(h,4)}\n"
    print(lines[i])
  f.close()
  f = open(filename,"w")
  f.writelines(lines)
  f.close()