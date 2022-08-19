# DigitDataProcessing


## Install

Setup virtual environment 
** Note that since development, pytorch3d 

```bash
python3.8 -m venv .venv/digit-processing-env
source .venv/digit-processing-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```



## Usage
```bash
python digitprocessing/convert_rosbag2json.py
python digitprocessing/align_log2imgs.py
python digitprocessing/downsample_log.py
```