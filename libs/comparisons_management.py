#! /usr/bin/python3

comp_filename = ""
elements_list = []
total_len = 0
l_fights = []
real_cmp_nb = 0


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

def local_dump_cmp():
	global real_cmp_nb
	real_cmp_nb += 1
	if(real_cmp_nb % 10 == 0):
		dump_comparisons(l_fights, f"{comp_filename}.cmp_sav")
		print("\n--- Dumped comparisons file ---")

def register_comparisons_filename(filename):
	global comp_filename
	comp_filename = filename

def register_list_comparisions(fights):
	global l_fights
	l_fights = fights

def register_elements_list(elements):
	global elements_list
	global total_len
	elements_list = elements
	total_len = len(elements_list)



def vote_for(l_score, l_sort, idxs):
	global l_fights
	if(len(l_fights) < total_len):
		l_fights = [[-1 for i in range(j)] for j in range(total_len)]
		register_list_comparisions(l_fights)


	glob_idxs = [elements_list.index(l_sort[idx]) for idx in idxs]
	# print(f"\n{glob_idxs}", end="")
	if(glob_idxs[0] < glob_idxs[1]):
		idxs[0], idxs[1] = idxs[1], idxs[0]
		glob_idxs[0], glob_idxs[1] = glob_idxs[1], glob_idxs[0]


	previous_index = l_fights[glob_idxs[0]][glob_idxs[1]]
	if(previous_index != -1):
		print(f"\n + Skipped vote ({l_sort[idxs[0]]} / {l_sort[idxs[1]]}) -> {l_sort[idxs[previous_index]]}")
		l_score[idxs[previous_index]]  += 1
		return idxs[previous_index]

	local_dump_cmp()
	
	res = input(f"\nChoose the best between {l_sort[idxs[0]]} and {l_sort[idxs[1]]}\nY - {l_sort[idxs[0]]}\n? - {l_sort[idxs[1]]}\n").lower()
	print()
	if(res == "y"):
		chosen_index = 0
	else:
		chosen_index = 1
  
	l_score[idxs[chosen_index]]  += 1
	print(f"{l_sort[idxs[chosen_index]]} Chosen")
	l_fights[glob_idxs[0]][glob_idxs[1]] = chosen_index

	return idxs[l_fights[glob_idxs[0]][glob_idxs[1]]]

def total_comparisons_this_session():
	return real_cmp_nb

def total_comparisions():
	nb_cmp = 0
	for cmp_list in l_fights:
		for elem in cmp_list:
			if elem != -1:
				nb_cmp += 1
	return nb_cmp

def calculate_winrates(list_comparisons):
	l_nb_fights = [0] * len(list_comparisons)
	l_fights_won = [0] * len(list_comparisons)
	for y in range(len(list_comparisons)):
		for x in range(0, y):
			if(list_comparisons[y][x] == -1):
				continue
			l_nb_fights[x] += 1
			l_nb_fights[y] += 1
			if(list_comparisons[y][x] == 0):
				l_fights_won[y] += 1
			else:
				l_fights_won[x] += 1
	return [l_fights_won[i] / l_nb_fights[i] if l_nb_fights[i] > 0 else 0 for i in range(len(list_comparisons))]

def calculate_global_winrates():
	return calculate_winrates(l_fights)

def sort_from_winrates(list_to_sort, list_comparisons):
	list_indexes = [i for i in range(len(list_to_sort))]
	l_sorted = []
	while(len(list_indexes) > 0):
		sub_comparisions = [[list_comparisons[y][x] for x in range(0,y) if x in list_indexes] for y in range(len(list_to_sort)) if y in list_indexes]
		sub_list_to_sort = [list_to_sort[i] for i in range(len(list_to_sort)) if i in list_indexes]
		winrates = calculate_winrates(sub_comparisions)
		idx_sorted = list_to_sort.index(sorted(zip(sub_list_to_sort, winrates), key=lambda elem: elem[1], reverse=True)[0][0])
		l_sorted.append(list_to_sort[idx_sorted])
		list_indexes.remove(idx_sorted)
	return l_sorted

def global_sort_from_winrates():
	return sort_from_winrates(elements_list, l_fights)


if __name__ == '__main__':
	import random
	max = 15
	l = [[i for i in range(max)] for j in range(max)]
	for _l in l:
		random.shuffle(_l)
	print(l)
	dump_comparisons(l, "test.txt")
	print(read_comparisons("test.txt"))