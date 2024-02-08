import argparse

from libs.comparisons_management import register_comparisons_filename, register_elements_list, register_list_comparisions, read_comparisons

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resume', help='Uses an existing comparisoins file to do comparisons', action='store_true')
parser.add_argument('-o', '--only-winrate', help='Prints only the list sorted by winrate after the original sort', action='store_true')
parser.add_argument('-w', '--winrate-display', help='Prints the list sorted by winrate after the original sort', action='store_true')
parser.add_argument('filename', help='bar help')

args = parser.parse_args()

def register_sort():

	file_src = open(args.filename, 'r')
	base_list = file_src.read().splitlines() 
	file_src.close()

	register_comparisons_filename(args.filename)
	register_elements_list(base_list)

	if(args.resume):
			print("Resumed")
			l_fights = read_comparisons(f"{args.filename}.cmp_sav")
			register_list_comparisions(l_fights)
			print(l_fights)

	return base_list

def can_display_winrate():
	return args.winrate_display or args.only_winrate

def can_display_base():
	return not args.only_winrate


