#! /usr/bin/python3
import random

from libs.comparisons_management import vote_for, calculate_global_winrates, global_sort_from_winrates
from libs.sort_cli_interface import register_sort, can_display_base, can_display_winrate


def sort_like(list_sort):
    length = len(list_sort)
    list_battles = [ (i, j) for i in range(length) for j in range(length) if i < j ]
    random.shuffle(list_battles)
    l_score = [0 for i in range(length)]
    print(list_battles)
    
    for idx1, idx2 in list_battles:
        vote_for(l_score, list_sort, [idx1, idx2])
    
    for i in range(length):
        print(f"{list_sort[i]} won {l_score[i]} fights")
     
    return [x for _,x in sorted(zip(l_score, list_sort))]

print("/!\\ This sort is untested aftem the comparisions modifications but this is so unefficient that I couldn't care less /!\\\n")

data = register_sort()

l_sorted = sort_like(data)
l_sorted.reverse()

print("\n\n================= FINAL RESULTS =================\n\n")
if can_display_base():
    print("Result from algorithm")
    for elem in l_sorted:
        print(elem)
        
if can_display_winrate():
    print("Result from winrate")
    print(f"List winrates:\n{calculate_global_winrates()}")
    for elem in global_sort_from_winrates():
        print(elem)