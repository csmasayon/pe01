#########################################################
#               Programming Exercise 01                 #
#                   Strings and DFA                     #
#                                                       #
#               Galang, Masayon, Poledo                 #
#########################################################
#   A program that recognizes strings based on given    #
#   deterministic finite automata.                      #
#########################################################

import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk

class StateMachine:
    """
    Class to represent a DFA and its processes.
    Main author: Poledo

    Attributes
    ----------
    alphabet : list[str]
        Contains the list of alphabets, list must be of length 2
    states : list[str]
        Contains a list of states in the DFA, state[0] is the start state
    f_states : list[str]
        Contains a list of final states
    transition : list[list[str]]
        Contains the transitions, i.e. transition[x][y] is destination state from 
        state[x] when alphabet[y] is inputted, second dimension must be of length 2
    
    Methods
    -------
    move(src, buf)
        Does the logic for state transitions
    is_final(state)
        Determines if a given state is final
    get_start_state()
        Gets the start state of the DFA
    """

    def __init__(self, alphabet: list[str], states: list[str], f_states: list[str], transition: list[list[str]]) -> None:
        """All parameters are assumed to be valid already. e.g., correct type, capitalized, correct length, etc.

        Parameters
        ----------
        alphabet : list[str]
            Contains the list of alphabets, list must be of length 2
        states : list[str]
            Contains a list of states in the DFA, state[0] is the start state
        f_states : list[str]
            Contains a list of final states
        transition : list[list[str]]
            Contains the transitions, i.e. transition[x][y] is destination state from 
            state[x] when alphabet[y] is inputted, second dimension must be of length 2
        """

        self.alphabet = alphabet
        self.states = states
        self.f_states = f_states
        self.transition = transition

    def move(self, src: str, buf: str) -> str:
        """Does the logic for state transitions

        Parameters
        ----------
        src : str
            Source state
        buf : str
            Input letter
        
        Raises
        ------
        Exception
            If an invalid state or input letter is passed

        Returns
        -------
        str
            destination state
        """

        if not src in self.states:
            raise Exception(f"Error! {src} is not a valid state.")
        if not buf in self.alphabet:
            raise Exception(f"Error! {buf} is not a valid input letter.")
        return self.transition[self.states.index(src)][self.alphabet.index(buf)]

    def is_final(self, state: str) -> bool:
        """Determines if a given state is final
    
        Parameters
        ----------
        state : str
            State to test

        Returns
        -------
        bool
            True if state is final state, false otherwise
        """

        if state in self.f_states:
            return True
        return False

    def get_start_state(self) -> str:
        """Gets the start state of the DFA

        Returns
        -------
        str
            The start state
        """

        return self.states[0]
    
    def format_for_display(self) -> list[list[str]]:
        """Saves the output as a properly formatted output.txt file
        
        Parameters
        ----------
        output_bools : list[bool]
            A list of bools from check_multiple() method
        """

        new_list = list()

        for state in self.states:
            current_line = list()
            if state == self.get_start_state():
                current_line.append('-')
                if self.is_final(state):
                    current_line[0] += '+'
            elif self.is_final(state):
                current_line.append('+')
            else:
                current_line.append('')
            current_line.append(state)
            current_line = current_line + self.transition[self.states.index(state)]
            new_list.append(current_line)
        
        return new_list


class FileParser:
    """
    A class that parses .in and .dfa files into usable elements in the program
    Main author: Poledo

    Methods
    -------
    in_parser(src)
        Parses a .in file
    dfa_parser(src)
        Parses a .dfa file
    """

    def in_parser(self, src: str) -> list[str]:
        """Parses a .in file
        
        Parameters
        ----------
        src : str
            A file path to the .in file
        
        Returns
        -------
        list[str]
            A list of all strings from the .in  file
        """

        file = open(src, 'r')
        content = file.read().splitlines()
        file.close()
        return content

    def dfa_parser(self, src: str) -> StateMachine:
        """Parses a .dfa file
        
        Parameters
        ----------
        src : str
            A file path to the .dfa file
        
        Raises
        ------
        Exception
            If there are invalid inputs in the file
        
        Returns
        -------
        StateMachine
            A working StateMachine object based on the .dfa file
        """

        file = open(src, 'r')
        content = file.read().splitlines()
        file.close()

        file_name = os.path.basename(src)

        for i in range(len(content)):
            content[i] = content[i].split(',')

        alphabet = content.pop(0)
        
        # errors: more than 2 symbols, the 2 symbols are the same, the symbols are not single character
        if (len(alphabet) != 2 or alphabet[0] == alphabet[1]):
            raise Exception(f"({file_name}) Invalid DFA! DFA must have 2 unique input symbols.")
        for char in alphabet:
            if (len(char) != 1):
                raise Exception(f"({file_name}) Invalid DFA! ({char}) is not a valid input symbol.")

        states = list()
        f_states = list()
        transition = list(list())

        start_state_found = False   # for checking invalid number of start states
        current_line = 1    # for checking dfa file line number

        for line in content:
            current_line += 1
            # error if line is missing state type or state name
            if len(line) < 2:
                raise Exception(f"({file_name}) Invalid DFA! Invalid state in line {current_line}.")
            if line[0] == '-' or line[0] == '-+' or line[0] == '+-':
                if start_state_found:
                    raise Exception(f"({file_name}) Invalid DFA! Duplicate start state in line {current_line}.")
                start_state_found = True
                states.insert(0, line[1])
                transition.insert(0, line[2:4])
                if line[0] == '-+' or line[0] == '+-':
                    f_states.append(line[1])
            else:
                if line[0] == '+':
                    f_states.append(line[1])
                elif line[0] != '':
                    # determinant of start/final state is not - or +
                    raise Exception(f"({file_name}) Invalid DFA! Invalid state type symbol ({line[0]}) in line {current_line}.")
                states.append(line[1])
                transition.append(line[2:4])
            
            # other errors: non capital letter state, invalid transitions
            if len(line[1]) != 1 or not line[1].isupper():
                raise Exception(f"({file_name}) Invalid DFA! Invalid state ({line[1]}) found in line {current_line}. Not a capital letter.")
            if len(line) != 4:
                raise Exception(f"({file_name}) Invalid DFA! Invalid number of state transitions in line {current_line}.")
        
        # some more errors: state with no transitions
        for line in transition:
            for state in line:
                if not state in states:
                    raise Exception(f"({file_name}) Invalid DFA! Invalid state ({state}) in transitions for state {states[transition.index(line)]}.")
        
        if not start_state_found:
            raise Exception(f"({file_name}) Invalid DFA! No start state found.")


        state_machine = StateMachine(alphabet, states, f_states, transition)
        return state_machine

class StringChecker:
    """
    A class that contains the methods for checking for valid strings
    Main author: Galang

    Methods
    -------
    is_valid(input, state_machine)
        Checks if a string is valid
    check_multiple(inputs, state_machine)
        Checks multiple strings if those are valid
    save_output(output_bools, filename)
        Saves the output as a properly formatted strings.out file
    """

    def is_valid(self, input: str, state_machine: StateMachine) -> bool:
        """Checks if a string is valid
        
        Parameters
        ----------
        input : str
            An input string to test
        state_machine : StateMachine
            A state machine object for recognizing valid words
        
        Returns
        -------
        bool
            True if string is valid, False otherwise
        """

        curr = state_machine.get_start_state()
        try:
            for i in range(len(input)):
                if ((input[i] == state_machine.alphabet[0] or input[i] == state_machine.alphabet[1]) == False):
                    return False
                curr = state_machine.move(curr,input[i])
            return state_machine.is_final(curr)
        except: # if error in move == crash == INVALID
            return False
    
    def check_multiple(self, inputs: list[str], state_machine: StateMachine) -> list[bool]:
        """Checks multiple strings if those are valid
        
        Parameters
        ----------
        input : list[str]
            A list of input strings to test
        state_machine : StateMachine
            A state machine object for recognizing valid words
        
        Returns
        -------
        list[bool]
            A list of bools per string, True if string is valid, False otherwise
        """

        boollist=[]
        for i in range(len(inputs)):
            if(self.is_valid(inputs[i],state_machine)):
                boollist.append(True)
            else:
                boollist.append(False)
        return boollist
    
    def save_output(self, output_bools: list[bool], filename: str) -> None:
        """Saves the output as a properly formatted output file
        
        Parameters
        ----------
        output_bools : list[bool]
            A list of bools from check_multiple() method
        filename : str
            The filename to store the outputs
        """

        file1 = open(filename, 'w')
        for i in range(len(output_bools)):
            if(output_bools[i] == True):
                file1.write("VALID\n")
            else:
                file1.write("INVALID\n")
        file1.close()

class App:
    """
    A class that represents the UI of the app
    Main author: Masayon

    Attributes
    ----------
    dfa : StateMachine
        A reference to the currently loaded dfa
    inputs : list[str]
        A list of input strings
    file_parser : FileParser
        A file parser object used to read .in and .dfa files
    string_checker : StringChecker
        A string checker object used to check the validity of strings given a dfa

    Methods
    -------
    update_status_bar(message)
        Changes the text in the status bar
    def load_file()
        Handles loading of files and displaying the outputs
    def process_file()
        Handles checking inputs to a dfa
    """

    def __init__(self) -> None:
        """Constructor of the App class 
        """

        # initialize instances of needed objects
        self.dfa = None
        self.inputs = None
        self.file_parser = FileParser()
        self.string_checker = StringChecker()

        # Create the main window
        root = tk.Tk()
        root.title("Strings and DFA")
        root.geometry("1000x515")

        last_successful_dfa = None
        default_headers = ["1", "2", "3", "4"]                

        # Create a custom style for buttons
        style = ttk.Style()
        style.configure("theme.TButton", font=("TkDefaultFont", 10, "bold"), padding=5)

        # Frame for the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(padx=20, pady=20)

        # A "Load File" button that loads only an .in or a .dfa file through a file manager window
        load_button = ttk.Button(button_frame, text="Load File", command=self.load_file, style="theme.TButton")
        load_button.grid(row=0, column=0, padx=5)

        # A "Process" button that processess the inputs to the DFA file
        process_button = ttk.Button(button_frame, text="Process", command=self.process_file, style="theme.TButton") #missing command for process
        process_button.grid(row=0, column=1, padx=5)

        # Frame for the status bar
        status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN, padx=5, pady=2)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Label for the status bar
        status_label = tk.Label(status_frame, text="STATUS:", anchor=tk.W, font=("TkDefaultFont", 10, "bold"))
        status_label.grid(row=0, column=0, sticky=tk.W)

        # Init state of status message label
        self.status_message_label = tk.Label(status_frame, text=" ", anchor=tk.W)
        self.status_message_label.grid(row=0, column=1, sticky=tk.W)

        # Create a frame for the transition table
        table_frame = tk.Frame(root)
        table_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=False)

        # Label for the transition table
        table_label = tk.Label(table_frame, text="Transition Table", font=("TkDefaultFont", 10, "bold"))
        table_label.pack()

        # Create the transition table using ttk.Treeview
        self.transition_table = ttk.Treeview(table_frame, columns=default_headers, show="headings", selectmode="browse")
        self.transition_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Insert the default column headers
        for header in default_headers:
            self.transition_table.heading(header, text=header)
            self.transition_table.column(header, width=50, minwidth=50, stretch=False)
            
        # Create a frame for the text areas on the right side
        text_area_frame = tk.Frame(root)
        text_area_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Label for the "Input" text area
        input_label = tk.Label(text_area_frame, text="Input", font=("TkDefaultFont", 10, "bold"))
        input_label.pack()

        # Create the "Input" text area
        self.input_text = tk.Text(text_area_frame, wrap=tk.WORD, height=10, width=40, state=tk.DISABLED)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Label for the "Output" text area
        output_label = tk.Label(text_area_frame, text="Output", font=("TkDefaultFont", 10, "bold"))
        output_label.pack()

        # Create the "Output" text area
        self.output_text = tk.Text(text_area_frame, wrap=tk.WORD, height=10, width=40, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True) 

        # Configure the grid weights to make widgets expand with window resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        text_area_frame.grid_rowconfigure(1, weight=1)
        text_area_frame.grid_columnconfigure(0, weight=1)

        root.mainloop()

    # Function to update the status bar text
    def update_status_bar(self, message: str) -> None:
        """Changes the text in the status bar

        Parameter
        ---------
        message : str
            Message to write in the status bar
        """

        self.status_message_label.config(text=message)
            
    # Function to load an .in or a .dfa file
    def load_file(self) -> None:
        """Handles loading of files and displaying the outputs
        """

        global last_successful_dfa
        global last_successful_dfa_name
        global input_name
        global input_path
        file_path = filedialog.askopenfilename(filetypes=[("*.in; *.dfa", "*.in *.dfa"),("Input Files (*.in)", "*.in"), ("DFA Files (*.dfa)", "*.dfa")])
        if file_path:
            file_extension = file_path.split('.')[-1]
            file_name = os.path.basename(file_path)
            if file_extension == "in":
                # self.load_in_file(file_path)
                self.inputs = self.file_parser.in_parser(file_path)
                input_path = file_path
                input_name = os.path.basename(input_path)
                
                self.input_text.config(state=tk.NORMAL) 
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, '\n'.join(self.inputs))
                self.input_text.config(state=tk.DISABLED)

                self.update_status_bar(f"Input from file {file_name} has been successfully loaded.")
            elif file_extension == "dfa":
                    # Check if it's a readable DFA file
                    try:
                        # Load and process the DFA file here
                        new_dfa = self.file_parser.dfa_parser(file_path)
                        last_successful_dfa = file_path
                        last_successful_dfa_name = os.path.basename(last_successful_dfa)
                        
                        self.dfa = new_dfa  

                        # Clear existing data and column headers
                        self.transition_table.delete(*self.transition_table.get_children())

                        # Read the first line to get column headers
                        column_headers = ["", "State", self.dfa.alphabet[0], self.dfa.alphabet[1]]
                        # self.transition_table["columns"] = column_headers

                        # Set column headers in the Treeview
                        for i, header in enumerate(column_headers):
                            self.transition_table.heading(f"#{i+1}", text=header)
                            self.transition_table.column(f"#{i+1}", width=50, minwidth=50)

                        # Read the rest of the file to populate the table
                        for line in self.dfa.format_for_display():
                            self.transition_table.insert("", "end", values=line)

                        # Set the width of the Treeview widget itself
                        self.transition_table.update_idletasks()  # Ensure column widths are applied
                        
                        self.update_status_bar(f"DFA table from {file_name} has been successfully loaded.")
                    except Exception as e:
                        if self.dfa is not None:
                            self.update_status_bar(f"Unable to load content from {file_name} due to invalid content. "
                                            f"The program will be using the content from the most recently successfully loaded {last_successful_dfa_name}.")
                            # self.load_dfa_file(last_successful_dfa)
                        else:
                            self.update_status_bar(f"Unable to load content from {file_name} due to invalid content.")
        else:   
            self.update_status_bar("Ready")

    def process_file(self) -> None:
        """Handles checking inputs to a dfa
        """

        if self.dfa is None or self.inputs is None:
            self.update_status_bar("Please load both a DFA file and an input file first.")
            return

        string_checker = StringChecker()
        output_bools = string_checker.check_multiple(self.inputs, self.dfa)
    
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        
        for index, valid in enumerate(output_bools): # index is needed here for enumerate(output_bools)
            if valid:
                self.output_text.insert(tk.END, f"VALID\n")
            else:
                self.output_text.insert(tk.END, f"INVALID\n")
        
        # change input.in to input.out for output filename
        output_name = input_name.split('.')
        output_name[len(output_name) - 1] = 'out'
        output_name = '.'.join(output_name)

        string_checker.save_output(output_bools, output_name)
        self.output_text.config(state=tk.DISABLED)

        self.update_status_bar(f"Input from {input_name} successfully processed using DFA table from {last_successful_dfa_name}. Output saved to {output_name}.")
            
# Create an app object
App()