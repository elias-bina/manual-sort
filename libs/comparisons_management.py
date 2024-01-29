#! /usr/bin/python3

def dump_comparisons(lists, file):
	with open(file, 'w') as file_hdl:
		for line in lists:
			for char in line:
				file_hdl.write(f"{char};")
			file_hdl.write("\n")


def read_comparisons(file):
	res = []
	with open(file, 'r') as file_hdl:
		data = file_hdl.readlines()
		for line in data:
			tmp_res = [int(char) for char in line.split(";") if char != "\n"]
			res.append(tmp_res)
	return res

comp_filename = ""
l_fights = []
real_cmp_nb = 0

def register_comparisons_filename(filename):
	global comp_filename
	comp_filename = filename

def register_list_comparisions(fights):
	global l_fights
	l_fights = fights

def local_dump_cmp():
	global real_cmp_nb
	real_cmp_nb += 1
	if(real_cmp_nb % 10 == 0):
		dump_comparisons(l_fights, f"{comp_filename}.cmp_sav")
		print("\n--- Dumped comparisons file ---")



def calculate_winrates(list_comparisons):
	pass


if __name__ == '__main__':
	import random
	max = 15
	l = [[i for i in range(max)] for j in range(max)]
	for _l in l:
		random.shuffle(_l)
	print(l)
	dump_comparisons(l, "test.txt")
	print(read_comparisons("test.txt"))