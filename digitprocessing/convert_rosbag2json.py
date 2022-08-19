import os
import json
import rosbag
import argparse



# Function to convert digit log file from ros bag to json
def convert_rosbag2json(input_bag_file, output_json_file):
	bag = rosbag.Bag(input_bag_file)

	output_directory = './digit_data_walking/aligned'

	data = {}
	# Iterate over all logger messages in the bag file 
	for topic, msg, t in bag.read_messages(topics=['/log_digit']):
		msg_time = int(str(msg.header.stamp))

		# Store digit configuration messages
		data[msg_time] = {
						  "q_all": list(msg.observation.q_all),
						  }
	bag.close()
	
	# Write data to json file
	with open(output_json_file, 'w') as f:
		json.dump(data, f)




if __name__=="__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--bag_file', type=str, nargs='?',
						default='./data/digit_data_walking/raw/digit_log.bag',
						help='string path to digit log bag file')
	parser.add_argument('--json_file', type=str, nargs='?',
						default='./data/digit_data_walking/raw/digit_log.json',
						help='string path to output log json file')
	args = parser.parse_args()


	convert_rosbag2json(args.bag_file, args.json_file)

