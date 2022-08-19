import os
import time
import json
import shutil
import argparse
import numpy as np


# Function to attempt creating a directory (agnostic of python version)
def trymakedirs(directory):
	try:
		os.makedirs(directory)
	except:
		pass


# Function to downsample, to 5hz, the already aligned rgb-depth images
def downsample_log(raw_directory, processed_directory, save_downsampled_imgs=False):

	if save_downsampled_imgs:
		output_rgb_directory = os.path.join(processed_directory,'downsampled','rgb')
		output_depth_directory = os.path.join(processed_directory,'downsampled','depth')
		trymakedirs(output_rgb_directory)
		trymakedirs(output_depth_directory)


	with open(os.path.join(processed_directory,'digit_log_aligned.json'), 'r') as f:
		data = json.load(f)

	q_times = sorted(list(data.keys()))


	time_counts = {}
	for img_i in range(len(q_times)):
		second = str(q_times[img_i])[:10]

		if second not in time_counts:
			time_counts[second] = []
		time_counts[second].append(q_times[img_i])


	inds_tot = 0
	data_downsampled = {}
	for t in time_counts.keys():
		
		options = sorted(time_counts[t])
		inds = np.round(np.linspace(0, len(options)-1, 5)).astype(int)

		for ind in inds:
			data_downsampled[inds_tot] = data[str(options[ind])]
			data_downsampled[inds_tot]["timestamp"] = str(options[ind])
			if save_downsampled_imgs:
				shutil.copy(os.path.join(os.path.join(raw_directory,'rgb'), str(options[ind])+'.png'), 
										os.path.join(output_rgb_directory, str(inds_tot)+'.png'))
				shutil.copy(os.path.join(os.path.join(raw_directory,'depth'), str(options[ind])+'.png'), 
										os.path.join(output_depth_directory, str(inds_tot)+'.png'))
			inds_tot += 1


	with open(os.path.join(processed_directory,'digit_log_downsampled.json'), 'w') as f:
		json.dump(data_downsampled,f)


	print(len(time_counts.keys())*5)
	print(inds_tot)


if __name__=="__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--raw_directory', type=str, nargs='?',
						default='./data/digit_data_walking/raw/',
						help='string path to digit data directory')
	parser.add_argument('--processed_directory', type=str, nargs='?',
						default='./data/digit_data_walking/processed/',
						help='string path to output processed directory')
	parser.add_argument('--save_downsampled_imgs', type=int, nargs='?',
						default=0,
						help='boolean to save output images')
	args = parser.parse_args()

	downsample_log(args.raw_directory, args.processed_directory,
				save_downsampled_imgs=args.save_downsampled_imgs)
