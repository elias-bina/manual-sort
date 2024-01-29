# Usage:

## Dependancies:

[Install python on your machine :)](https://www.google.com/search?client=firefox-b-e&q=how+to+install+python)

## Launch:

You may use any of the sort algorithm by launching the `<sort-name>-sort.py` file associated and having your list to sort as the first argument.
Examples of said lists can be found in `./example-list-to-sort` (It's literally just a list of strings)

There is a tournament sort only (for now) feature:
The algorithm stores automatically the results of your comparisons in a `.cmp_sav` file, and by adding the cli option "resume", you can use a pre-existing `.cmp_sav` file to bypass already made comparisons

There is an `expand-cmp-list.py` which allows to add some terms to your existing comparisons list


# TODO:

- Add an "error checker" which looks at a comparisons file, and check that the comparisons with the winrate differences are the most wrong according to the comparison are re-manually check

- Have a real modules organization (global variables bad bla bla bla)

- Align all algorithms CLI API by creating a library (for example at least the resume option) 

- Create an option to display the results by winrate whatever the algorithm is

- Test "Winrate sort" -> At first make "random" matches (create a pool, take pairs, rince, repeat), and when there are some little stats, sort by winrate and fight between games with similar winrates (before this step), and show the results each X waves

- Android app in react native with machine learning & NFTs but no ads

# Support:

Feel free to open issues if you feel something is missing
