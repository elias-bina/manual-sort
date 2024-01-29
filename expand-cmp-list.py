#! /usr/bin/python3
import sys

from libs.comparisons_management import dump_comparisons, read_comparisons


def dump_file_list(base_list, file_name):
	with open(file_name, 'w') as file_hdl:
		for line in base_list:
			file_hdl.write(f"{line}\n")


def add_element(base_list, l_fights):
	while True:
		name = input(f"\nGive the name you want to add in the list\n")
		in_list = False
		for elem in base_list:
			if elem.lower() == name.lower():
				in_list = True		
				break

		if not in_list:
			break
		print(f"{name} is already in the list")

	l_fights.append([-1 for i in range(len(l_fights[-1]) + 1)])
	base_list.append(name)
	print(f"{name} added to the list")



file_src = open(sys.argv[1], 'r')
base_list = file_src.read().splitlines() 
file_src.close()

l_fights = read_comparisons(f"{sys.argv[1]}.cmp_sav")
for line in l_fights:
	print(line)
 
while 1:
	add_element(base_list, l_fights)
	dump_comparisons(l_fights, f"{sys.argv[1]}.cmp_sav")
	dump_file_list(base_list, sys.argv[1])