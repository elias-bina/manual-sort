#! /usr/bin/python3
import random

from libs.comparisons_management import vote_for, total_comparisons_this_session, total_comparisions, \
										calculate_global_winrates, global_sort_from_winrates

from libs.sort_cli_interface import register_sort, can_display_base, can_display_winrate, is_resumed

from libs.sort_algorithms import full_manual_sort

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
	"""
		Get a pair of elements from lists with opposed ranks, only if the two rank lists are not empty
		If they are, take two random elements from most remplished lists
	"""

	i_max = get_most_remplished_list(list_ranks)
	
	while i_max < len(list_ranks) and (len(list_ranks[len(list_ranks) - i_max - 1]) <= 0 or len(list_ranks[i_max]) <= 0):
		i_max +=1
	
	if i_max < len(list_ranks):
		return [list_ranks[i_max].pop(0), list_ranks[len(list_ranks) - i_max - 1].pop(0)]
	else:
		return [get_outlier(list_ranks), get_outlier(list_ranks)]

def translate_groups(list_groups):
	"""
		Create a list of ranks (list of firsts, list of seconds...) from the list of groups (manually fully sorted lists)
	"""
	list_ranks = []
	while len(list_groups[0]):
		list_ranks.append([group.pop(0) for group in list_groups if len(group) > 0])

	for rank_list in list_ranks:
		random.shuffle(rank_list)

	return list_ranks


def prepare_tournament_from_ranks_recur(n, list_ranks):
	# If on a leaf, either get an element alone (a random element from the most remplished list that will not do the fight), 
	# or have a comparison created from opposed pairs (ex if 8 ranks, 1vs8 , 2vs7 etc)
	if n == 1:
		return [get_outlier(list_ranks)]
	if n == 2:
		return get_opposed_pair(list_ranks)

	# Create a list of tournaments, that contains list of tournaments
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
	"""
		Recursively find the maximum depth of the tournament list by detecting if the element is a list
	"""
	if not isinstance(list_tournaments[0], list):
		return max_depth
	return max([find_tournament_list_depth(max_depth + 1, l_tournament) for l_tournament in list_tournaments])


def run_tournament_step_matchs(depth_to_go, list_tournaments):
	"""
		Creates a list of loosers from a tournaments, while modifying in place the list of tournaments,
		lowering the max depth of these tournaments by one
	"""

	loosers = []
	# If just before a leaf, run tournaments, either by voting for a winner (and adding a looser),
	# either automatically winning if alone.
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
	
	# Find loosers from sub tournament. Lower depth tournaments will be ignored, not have any loosers
	# but be picked when the global max depth will be lowered
	for sub_tournament in list_tournaments:
		loosers += run_tournament_step_matchs(depth_to_go - 1, sub_tournament)
	return loosers

def run_tournament_step(list_tournaments, step_depth):
	"""
		Recursively run the tournaments, taking the list of tournaments and outputing the "sorted" flat list
	"""

	# If on a leaf, run the leaf comparison
	if(step_depth == 0):
		if(len(list_tournaments) > 2):
			assert("Cringe man")
		if(len(list_tournaments) == 1):
			return [list_tournaments[0]]
		voted = vote_for([0,0], list_tournaments, [0, 1])
		return [list_tournaments[voted], list_tournaments[1 - voted]]

	# If not, run the full remaining tournament and get the loosers list
	looser_list = run_tournament_step_matchs(step_depth, list_tournaments)

	# The final list is the result of winners tournament, followed of the result of the looser tournament
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
		# Do a full sort
		list_groups[i] = full_manual_sort(list_groups[i])
		list_groups[i].reverse()
		print(list_groups[i])
	return list_groups


def sort_tournament(list_sort):
	return tournament_phase(group_phase(list_sort))




if __name__ == "__main__":
	base_list = register_sort()
	total_len = len(base_list)

	if(can_display_winrate() and is_resumed()):
		print("Result from winrate\n")
		print(f"List winrates:\n{calculate_global_winrates()}\n\n")
		for elem in global_sort_from_winrates():
			print(elem)
		print(f"\nNumber of comparisions this session:{total_comparisons_this_session()}; Total comparisions:{total_comparisions()} (Max:{total_len * (total_len- 1) / 2})")

	ranking_global = dict()
	l_sorted = sort_tournament(base_list)
	for i in range(len(l_sorted)):
		ranking_global[l_sorted[i]] = i

	while 1:
		print("\n\n================ TOURNAMENT RESULTS (continue to refine results) ================\n\n")
		if can_display_base():
			print("Result from algorithm\n")
			print(ranking_global)
			print("\n")
			for elem in dict(sorted(ranking_global.items(), key=lambda x:x[1])):
				print(elem)
			print("\n\n")


		if can_display_winrate():
			print("Result from winrate\n")
			print(f"List winrates:\n{calculate_global_winrates()}\n\n")
			for elem in global_sort_from_winrates():
				print(elem)
			print(f"\nNumber of comparisions this session:{total_comparisons_this_session()}; Total comparisions:{total_comparisions()} (Max:{total_len * (total_len- 1) / 2})")

		l_sorted_repeat = sort_tournament(base_list)
		for i in range(len(l_sorted_repeat)):
			ranking_global[l_sorted_repeat[i]] += i

