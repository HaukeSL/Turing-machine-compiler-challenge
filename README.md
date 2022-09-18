# Turing-machine-compiler-challenge
Turing-machine-compiler-challenge IBE150. 2022-09-18

Challenge:
Make a program in Python or JupyterLab that takes a text file with PT-system states as input and returns them as TM-states.
Test the turing machine of the compiler with the program from challenge 1. 

Obs Obs! 
I altered the program from challenge 1. It takes a dictionary as input instead of a list. 
It made the code of the compile function a bit more comprehensible. 

PT states for double 1 problem: 
1: print 0
2: go left
3: goto step 1 if cell is 1
4: print 1
5: go right
6: goto step 1 if cell is 1
7: goto step 4 if cell is 0
8: stop

Compiled to TM states( r_ = subroutines)
1: print_0
2: r_goright
3: goleft
4: goto_step_1_if_cell_is_1
5: r_goright step 0 if cell is 1
6: r_goright step 7 if cell is not 1
7: print_1
8: r_goright
9: goright
10: goto_step_1_if_cell_is_1
11: r_goright step 0 if cell is 1
12: r_goright step 12 if cell is not 1
13: goto_step_4_if_cell_is_0
14: r_goright step 7 if cell is 1
15: r_goright step 16 if cell is not 1
16: e
