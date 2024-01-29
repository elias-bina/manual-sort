#! /usr/bin/python3
import sys
import random

from libs.comparisons_management import local_dump_cmp, read_comparisons, register_comparisons_filename, register_list_comparisions

real_cmp_nb = 0

# After, test to : https://www.baeldung.com/cs/tournament-sort-algorithm
#                  https://en.oi-wiki.org/basic/tournament-sort/
#
# And read       : https://www.semanticscholar.org/paper/Robustness-versus-Performance-in-Sorting-and-Elmenreich-Ibounig/d643d03e3ff681de87738401eca12814eff7d71f
#                  https://cs.stackexchange.com/questions/142075/what-is-a-sorting-algorithm-that-is-robust-to-a-faulty-comparison

def tri_fusion(liste):
	n = len(liste)
	if n == 1:
		return liste
	else:
		return fusion([tri_fusion(liste[:n//2]),tri_fusion(liste[n//2:])])

def fusion(lists):
	liste_res = []
	idxs = [0, 0]
	while(len(lists[0]) > idxs[0] and len(lists[1]) > idxs[1]):
		res = vote_for([0,0], [lists[0][idxs[0]], lists[1][idxs[1]]], [0, 1])
		liste_res.append(lists[res][idxs[res]])
		idxs[res] +=1

	for j in range(2):
		for i in range(idxs[j], len(lists[j])):
			liste_res.append(lists[j][i])

	return liste_res




# TODO: Move this in comparisons_management (register baselist func, etc ?)
l_fights=[]

def vote_for(l_score, l_sort, idxs):
	global l_fights
	if(len(l_fights) < total_len):
		l_fights = [[-1 for i in range(j)] for j in range(total_len)]
		register_list_comparisions(l_fights)


	glob_idxs = [base_list.index(l_sort[idx]) for idx in idxs]
	print(f"\n{glob_idxs}", end="")
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



def sort_like(list_sort):
	length = len(list_sort)
	list_battles = [ (i, j) for i in range(length) for j in range(length) if i < j ]
	random.shuffle(list_battles)
	l_score = [0 for i in range(length)]
	
	for idx1, idx2 in list_battles:
		vote_for(l_score, list_sort, [idx1, idx2])
	
	# for i in range(length):
	# 	print(f"{list_sort[i]} won {l_score[i]} fights")
	 
	return [x for _,x in sorted(zip(l_score, list_sort))]



def get_most_remplished_list(lists):
	i_max, maximum = 0, len(lists[0])
	for i in range(len(lists)):
		g_len = len(lists[i])
		if g_len > maximum:
			maximum = g_len
			i_max = i
	return i_max

def get_outlier(list_ranks):
	return list_ranks[get_most_remplished_list(list_ranks)].pop(0)

def get_opposed_pair(list_ranks):
	i_max = get_most_remplished_list(list_ranks)
	
	while i_max < len(list_ranks) and (len(list_ranks[len(list_ranks) - i_max - 1]) <= 0 or len(list_ranks[i_max]) <= 0):
		i_max +=1
	
	if i_max < len(list_ranks):
		return [list_ranks[i_max].pop(0), list_ranks[len(list_ranks) - i_max - 1].pop(0)]
	else:
		return [get_outlier(list_ranks), get_outlier(list_ranks)]

def translate_groups(list_groups):
	list_ranks = []
	while len(list_groups[0]):
		list_ranks.append([group.pop(0) for group in list_groups if len(group) > 0])

	for rank_list in list_ranks:
		random.shuffle(rank_list)

	return list_ranks


def prepare_tournament_from_ranks_recur(n, list_ranks):
	if n == 1:
		return [get_outlier(list_ranks)]
	if n == 2:
		return get_opposed_pair(list_ranks)

	return [prepare_tournament_from_ranks_recur(n//2, list_ranks), prepare_tournament_from_ranks_recur(n - n//2, list_ranks)]

def prepare_tournament_from_ranks(list_groups):
	list_ranks = translate_groups(list_groups)
	return prepare_tournament_from_ranks_recur(total_len, list_ranks)

def prepare_tournament_from_flat_recur(n, flat_list):
	if n == 1:
		return [flat_list.pop(0)]
	if n == 2:
		return [flat_list.pop(0), flat_list.pop(0)]
	return [prepare_tournament_from_flat_recur(n//2, flat_list), prepare_tournament_from_flat_recur(n - n//2, flat_list)]

def prepare_tournament_from_flat(flat_list):
	return prepare_tournament_from_flat_recur(len(flat_list), flat_list)

# TODO: Test it 
def find_tournament_list_depth(max_depth, list_tournaments):
	if not isinstance(list_tournaments[0], list):
		return max_depth
	return max([find_tournament_list_depth(max_depth + 1, l_tournament) for l_tournament in list_tournaments])


def run_tournament_step_matchs(depth_to_go, list_tournaments):
	loosers = []
	if(depth_to_go == 1):
		if not isinstance(list_tournaments[0], list):
			return []
		for i in range(len(list_tournaments)):
			if(len(list_tournaments[i]) == 1):
				list_tournaments[i] = list_tournaments[i][0]
			else:
				voted = vote_for([0,0], list_tournaments[i], [0, 1])
				loosers += [list_tournaments[i][1 - voted]]
				list_tournaments[i] = list_tournaments[i][voted]
		return loosers
	

	for sub_tournament in list_tournaments:
		loosers += run_tournament_step_matchs(depth_to_go - 1, sub_tournament)
	return loosers

def run_tournament_step(list_tournaments, step_depth):
	if(step_depth == 0):
		if(len(list_tournaments) > 2):
			assert("Cringe man")
		if(len(list_tournaments) == 1):
			return [list_tournaments[0]]
		voted = vote_for([0,0], list_tournaments, [0, 1])
		return [list_tournaments[voted], list_tournaments[1 - voted]]
	looser_list = run_tournament_step_matchs(step_depth, list_tournaments)
	return run_tournament_step(list_tournaments, step_depth - 1) + run_tournament(prepare_tournament_from_flat(looser_list))

def run_tournament(list_tournaments):
	return run_tournament_step(list_tournaments, find_tournament_list_depth(0, list_tournaments))

def tournament_phase(list_groups):
	## Post group_phase first_phase_tournament
	list_tournaments = prepare_tournament_from_ranks(list_groups)
	return run_tournament(list_tournaments)



def prepare_groups(list_sort):
	data = [i for i in list_sort]
	random.shuffle(data)
	nb_elems = len(data)
	size_groups = 2
	while size_groups * size_groups < nb_elems:
		size_groups += 2
	if(size_groups > 2):
		size_groups -= 2


	nb_groups = nb_elems // size_groups
	list_groups = []
	for group_idx in range(nb_groups):
		list_groups.append(data[size_groups * group_idx:size_groups * (group_idx + 1)])
	if(nb_groups*size_groups != nb_elems):
		list_groups.append(data[nb_groups*size_groups:])

	print(f"Size of groups: {size_groups}; Nb groups: {len(list_groups)}")

	return list_groups


def group_phase(list_sort):
	list_groups = prepare_groups(list_sort)
	for i in range(len(list_groups)):
		list_groups[i] = sort_like(list_groups[i])
		list_groups[i].reverse()
		print(list_groups[i])
	return list_groups




def sort_tournament(list_sort):
	return tournament_phase(group_phase(list_sort))



file_src = open(sys.argv[1], 'r')
base_list = file_src.read().splitlines() 
file_src.close()

if(len(sys.argv) >= 3):
	if(sys.argv[2] == "resume"):
		print("Resumed")
		l_fights = read_comparisons(f"{sys.argv[1]}.cmp_sav")
		register_list_comparisions(l_fights)
		print(l_fights)


# data = [i for i in range(120)]
total_len = len(base_list)

register_comparisons_filename(sys.argv[1])

ranking_global = dict()
l_sorted = sort_tournament(base_list)
for i in range(len(l_sorted)):
	ranking_global[l_sorted[i]] = i

# TODO:Find a finer way to get outliers out -> chose those with most winrate ? -> Create groups from sorted ?
# TODO: Sort by winrate ?
while 1:
	print("\n\n================ TORNAMENT RESULTS (continue to refine results) ================\n\n")
	print(ranking_global)
	for elem in dict(sorted(ranking_global.items(), key=lambda x:x[1])):
		print(elem)
	print(f"\n Number of comparisions:{real_cmp_nb} (Max:{total_len * (total_len - 1) / 2})")
	
	l_sorted_repeat = sort_tournament(base_list)
	for i in range(len(l_sorted_repeat)):
		ranking_global[l_sorted_repeat[i]] += i
