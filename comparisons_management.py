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


if __name__ == '__main__':
	import random
	max = 15
	l = [[i for i in range(max)] for j in range(max)]
	for _l in l:
		random.shuffle(_l)
	print(l)
	dump_comparisons(l, "test.txt")
	print(read_comparisons("test.txt"))