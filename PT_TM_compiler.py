import time

#pretty output with colors *.*
class bcolors:
    OKBLUE = '\033[94m'  # blue
    OKGREEN = '\033[92m'  # green
    RED = '\033[91m'  # red
    ENDC = '\033[0m'  # white

def visual_head_moves(tape: list, curr_pos: int, curr_val: int, instruc_val: int) -> None: 
    string = ""
    colortape = list(tape)

    for j in range(0, len(colortape)):
        if j == curr_pos:
            if curr_val != instruc_val:
                    if curr_val == " ":
                        string = string+"|"+ bcolors.RED + "B"+ bcolors.ENDC
                    else:
                        string = string+"|"+ bcolors.RED + colortape[j]+ bcolors.ENDC
            else:
            
                if curr_val == " ":
                    string = string+"|"+ bcolors.OKBLUE+ "B"+ bcolors.ENDC 
                else:
                    string = string+"|"+ bcolors.OKBLUE + colortape[j]+ bcolors.ENDC
        else:
            string = string +"|"+ colortape[j]
    print(string)
    
# L/R values           
L = - 1
R = + 1

def compile() -> dict:
    """
    Input: txt file with PT states as pt_txt
    Output: dictionary with TM states 
    """
    pt_txt = open("input.txt")
    str_states = []
    new_q_dict = {}
    TM_line_counter = 0
    PT_line_counter = 0
    PT_vs_TM = {PT_line_counter: TM_line_counter}

    for line in pt_txt:
        line = line.strip()

        # compiling go left
        if "go left" in line:
            new_q_dict[str(TM_line_counter)+line] = {
            '1': ['1', -1, TM_line_counter +1],
            '0': ['0', -1, TM_line_counter +1],
            ' ': [' ', -1, TM_line_counter +1]
            }
            str_states.append(str(TM_line_counter)+line)

        # compiling go right
        elif "go right" in line:  
            new_q_dict[str(TM_line_counter)+line] = {
            '1': ['1', 1, TM_line_counter +1],
            '0': ['0', 1, TM_line_counter +1],
            ' ': [' ', 1, TM_line_counter +1]
            } 
            str_states.append(str(TM_line_counter)+line) 

        # compiling go to x if cell is x
        elif "goto" in line: 
            
            new_q_dict[str(TM_line_counter)+line] = {
                "1": ["1", L, TM_line_counter+2],
                "0": ["0", L, TM_line_counter+2],
                " ": [" ", L, TM_line_counter+2]}
            str_states.append(str(TM_line_counter)+line)
            
            for i in new_q_dict[str(TM_line_counter)+line]:
                if i == line[-1]:
                    new_q_dict[str(TM_line_counter)+line][i] = [line[-1],L,TM_line_counter+1]

            TM_line_counter += 1

            new_q_dict[str(TM_line_counter)+"r_goright"] = {
                "1": ["1", R, PT_vs_TM[int(line[10])-1]],
                "0": ["0", R, PT_vs_TM[int(line[10])-1]],
                " ": [" ", R, PT_vs_TM[int(line[10])-1]]}
            str_states.append(str(TM_line_counter)+"r_goright")
            TM_line_counter += 1
            

            new_q_dict[str(TM_line_counter)+"r_goright"] = {
                "1": ["1", R, TM_line_counter+1],
                "0": ["0", R, TM_line_counter+1],
                " ": [" ", R, TM_line_counter+1]}
            str_states.append(str(TM_line_counter)+"r_goright")
        # compiling stop           
        elif "stop" in line: 
            str_states.append(line)
            new_q_dict[line] = {
                "1": ["1", L, -1],
                "0": ["0", L, -1],
                " ": [" ", L, -1]}
        #compiling print x
        elif "print" in line:
            new_q_dict[str(TM_line_counter)+line] = {
                "1": [line[-1], L, TM_line_counter+1],
                "0": [line[-1], L, TM_line_counter+1],
                " ": [line[-1], L, TM_line_counter+1]}
            str_states.append(str(TM_line_counter)+line)

            new_q_dict[str(TM_line_counter)+"r_goright"] = {
                "1": ["1", R, TM_line_counter+2],
                "0": ["0", R, TM_line_counter+2],
                " ": [" ", R, TM_line_counter+2]}
            str_states.append(str(TM_line_counter)+"r_goright")
            TM_line_counter += 1
            
        PT_line_counter += 1
        TM_line_counter += 1
        PT_vs_TM[PT_line_counter] = TM_line_counter


    # print("\n",str(new_q_dict).replace(": {",":\n{"))
    # print("\n", str_states) 
    # print(PT_vs_TM)
    pt_txt.close()
    return new_q_dict

def tape_create():
    """
    Input: user input
    Output: list of a TM tape 
    """
    user_input = input("Enter input: ")
    tape_list = [" ", " ", " ", " "]
    i = 0
    while i < len(user_input):
        if user_input[i] != "0" and user_input[i] != "1":
            user_input = input("Wrong value detected. Enter only 0s and/or 1s. Try again: ")
            i = 0
        else:
            tape_list.insert(-3, user_input[i])
            tape_list.insert(0, " ")

        i += 1

    return tape_list

def find_start(tape: list):
    """
    Case: find start cell at first non-blank value on tape
    input: tape
    output: returns index of first non-blank value on the tape array
    """
    if len(tape) > 0:
        for i in range(len(tape)):
            if tape[i] != " ":
                return i
    return 0

# Turing machine programm

def turingmachine(org_tape: list,instructions: dict) -> list:
    """
    Input: dictionary of states, tape.
    Output: list of altered tape
    Method: while loop, making each step equivalent to a Turing Machine
    """
    start = time.time()
    tape = list(org_tape)
    step_counter = 0  # counting loop iteration
    curr_state = instructions[list(instructions)[0]]  # start state
    curr_pos = find_start(tape)  # start position
    curr_val = tape[curr_pos]  # value at start position
    instruc_val = curr_state[curr_val][0]  # the value which shall be inserted

    # while loop stops if next state is -1, like in q23:{" ": " ", L, -1}
    while curr_state[curr_val][2] != -1:
        # time.sleep(0.1)

        #function to visualize the tape in the console output
        visual_head_moves(tape, curr_pos,curr_val, instruc_val)

        # 1 writes instructed value to tape
        tape[curr_pos] = instruc_val

        # 2 continues to next position as instructed(L/R)
        curr_pos += curr_state[curr_val][1]

        # 3 continues with instructed next state
        curr_state = instructions[list(instructions)[curr_state[curr_val][2]]]

        # 4 reads value of the current position (1,0,b)
        curr_val = tape[curr_pos]

        # 5 updating the instruction value from current state
        instruc_val = curr_state[curr_val][0]

        # step counter increment
        step_counter += 1
        # print(list(instructions)[curr_state[curr_val][2]])

    visual_head_moves(tape, curr_pos,curr_val, instruc_val)
    print(bcolors.OKBLUE,"\nTotal of", step_counter,"steps. At", str(len(instructions)),"TM states.", bcolors.ENDC)

    end = time.time()
    print(round((end - start)*1000,2), "ms elapsed.(Sleep timer on/off?)")
    return tape

turingmachine(tape_create(), compile())
