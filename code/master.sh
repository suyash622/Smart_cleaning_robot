

## Master run for entire pipeline
## 1. Download the pcd file.
## 2. Perform cleaning,filtering and clustering and generate waypoints.
## 3. Perform path planning, get path and HTML.
## 4. Load link of HTML to the server.

python ./download.py  
python ./convert.py
python ./cord1.py 
python ./master_1.py --display 0 --animate 1 
python ./upload_ser.py 
# python cv.py --fil points_inliers_r.pcd
