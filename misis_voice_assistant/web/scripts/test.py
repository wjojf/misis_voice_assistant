user_data_filepath = '../assets/passwords/curr_password.txt'

with open(user_data_filepath, 'r') as file:
	print(file.readlines())