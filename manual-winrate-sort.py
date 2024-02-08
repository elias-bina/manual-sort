#! /usr/bin/python3

from libs.comparisons_management import vote_for, total_comparisons_this_session, \
										calculate_global_winrates, global_sort_from_winrates
from libs.sort_cli_interface import register_sort, can_display_base, can_display_winrate

def first_winrate_pass(base_list):
	l_indexes = [i for i in range(len(base_list))]
	

def sort_winrate(base_list):
	winrates = calculate_global_winrates()
	if(winrates == []):
		first_winrate_pass(base_list)
		winrates = calculate_global_winrates()
	print(winrates)


base_list = register_sort()
l_sorted = sort_winrate(base_list)

total_len = len(base_list)

while 1:
	print("\n\n================ TORNAMENT RESULTS (continue to refine results) ================\n\n")
	if can_display_base() or can_display_winrate():
		print("Result from algorithm (same as winrate)")
		print(f"List winrates:\n{calculate_global_winrates()}")
		for elem in global_sort_from_winrates():
			print(elem)
		print(f"\n Number of comparisions:{total_comparisons_this_session()} (Max:{ total_len * (total_len- 1) / 2})")
