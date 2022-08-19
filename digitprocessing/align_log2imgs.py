import os
import json
import shutil
import argparse

# Function to attempt creating a directory (agnostic of python version)
def trymakedirs(directory):
	try:
		os.makedirs(directory)
	except:
		pass

# Function to align time stamps from digit log file to stored rgb-depth images 
def align_log2imgs(raw_directory, processed_directory,
				  start_stamp_log, end_stamp_log, 
				  start_stamp_rgb, end_stamp_rgb,
				  save_aligned_imgs=False):

	with open(os.path.join(raw_directory, 'digit_log.json'), 'r') as f:
		data = json.load(f)

	q_times = sorted(list(data.keys()))
	q_times = [int(q) for q in q_times]
	q_times = q_times[q_times.index(start_stamp_log):q_times.index(end_stamp_log)+1]


	if save_aligned_imgs:
		output_rgb_directory = os.path.join(processed_directory,'aligned','rgb')
		output_depth_directory = os.path.join(processed_directory,'algined','depth')
		trymakedirs(output_rgb_directory)
		trymakedirs(output_depth_directory)

	input_depth_directory = os.path.join(raw_directory, 'depth')
	input_rgb_directory = os.path.join(raw_directory, 'rgb')

	rgb_depth_imgs = sorted(list(set(os.listdir(input_depth_directory)).intersection(set(os.listdir(input_rgb_directory)))))
	rgb_depth_imgs = rgb_depth_imgs[rgb_depth_imgs.index(str(start_stamp_rgb)+'.png'):rgb_depth_imgs.index(str(end_stamp_rgb)+'.png')+1]
	rgb_depth_times = [int(img_name.split('.')[0]) for img_name in rgb_depth_imgs]

	q_times_shifted = [t-start_stamp_log for t in q_times]
	rgb_depth_times_shifted = [t-start_stamp_rgb for t in rgb_depth_times]

	data_aligned = {}


	for img_i in range(len(rgb_depth_imgs)):
	
		closest_idx = 0
		min_delta = 9999999999999999999
		stop_delta = 9999999999999999999

		for q_i in range(len(q_times)):
			pair_delta = abs(rgb_depth_times_shifted[img_i]-q_times_shifted[q_i])
			# Record the current closest index
			if pair_delta < min_delta:
				min_delta = pair_delta
				closest_idx = q_i
			# If the current delta begins to increase, then stop the linear search
			if pair_delta>stop_delta:
				break
			# Store the current delta for use in recognizing when it begins to increase
			stop_delta = pair_delta
		
		data_aligned[str(rgb_depth_times[img_i])] = data[str(q_times[closest_idx])]

		if save_aligned_imgs:
			shutil.copy(os.path.join(input_rgb_directory, rgb_depth_imgs[img_i]), output_rgb_directory)
			shutil.copy(os.path.join(input_depth_directory, rgb_depth_imgs[img_i]), output_depth_directory)

	with open(os.path.join(processed_directory,'digit_log_aligned.json'), 'w') as f:
		json.dump(data_aligned,f)



if __name__=="__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--raw_directory', type=str, nargs='?',
						default='./data/digit_data_walking/raw/',
						help='string path to digit data directory')
	parser.add_argument('--processed_directory', type=str, nargs='?',
						default='./data/digit_data_walking/processed/',
						help='string path to output processed directory')
	parser.add_argument('--start_stamp_log', type=int, nargs='?',
						default=1657563058818765328,
						help='integer ros-time at aligned first frame in log file')
	parser.add_argument('--end_stamp_log', type=int, nargs='?',
						default=1657563235483763183,
						help='integer ros-time at aligned last frame in log file')
	parser.add_argument('--start_stamp_rgb', type=int, nargs='?',
						default=1657558742649914980,
						help='integer ros-time at aligned first frame in raw rgb-depth directories')
	parser.add_argument('--end_stamp_rgb', type=int, nargs='?',
						default=1657558918829205990,
						help='integer ros-time at aligned last frame in raw rgb-depth directories')
	args = parser.parse_args()

	align_log2imgs(args.raw_directory, args.processed_directory,
					args.start_stamp_log, args.end_stamp_log,
					args.start_stamp_rgb, args.end_stamp_rgb)
