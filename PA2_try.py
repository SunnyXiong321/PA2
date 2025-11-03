'''
PA2 --  Periodic Review
By: Sunny Xiong
What it does: It creates a flashcards for chemistry students to study for periodic table, 
where it'll provide the symbol and user answers the name
By doing this, the program needs to reads the text from either csv or txt files, play the 
flashcard game out, and record user history.
What went well: once the structure is clear, the coding became easy, the formatting part 
and the read files from csv/txt part is not hard
what would have made it even better: I would maybe create more decks for different classes 
for better user experience.
what you would do with more time to work: format it better, add some effects if they got right/wrong.
pledge: I neither given nor received help on this assignment except i let my friends look through and 
peer reviewed, I went on google and youtube to find tutorials, and went over with Mx.K.

'''


import time #record the time to save score
import random #shuffle the flashcards
final_score = 0 
question_total = 0
file_name = ""


def parse_line(line):
        
    '''
    - Takes one line of text and tries to extract a flashcard pair.
    - accepts format: term,definition

    Parameters:
    line (str)

    Returns:
    if valid = (term, definition)   
    if invalid = None
    '''


    line = line.strip() # remove spaces & newline around the text
    if line == "": # ignore empty lines
        return None

    # accept only "term,definition" format
    if "," in line:
        parts = line.split(",", 1)  # split only at first comma
    else:
        return None # no comma = not a valid card

    term = parts[0].strip()
    definition = parts[1].strip()

    if term and definition:  # both pieces must exist
        return term, definition  # return both values together

    return None # missing either piece = skip 


def play_quiz(filename):
    '''
    Parameters:
    filename (str)

    Returns:
    score (int) → number correct
    -1 → quit early
    None → file error or empty deck
    '''

    global file_name, final_score, question_total  # allow function to update globals used later for saving scores

    try:  # try reading file; prevents crash if user typed wrong filename
        with open(filename, "r") as f:  # open the deck in read-only mode
            lines = f.readlines()  # read entire file into a list of lines
    except FileNotFoundError:
        print("File not found. Please check your spelling and try again.")
        return None  


    flashcards = []  
    for line in lines: 
        parsed = parse_line(line) # use helper to extract term + definition
        if parsed is None:  # skip lines that are blank or incorrectly formatted
            continue
        term, definition = parsed 
        flashcards.append([term, definition])    # store as a 2-item list
 
    if not flashcards:
        print("No valid flashcards found in this file.")
        return None

    file_name = filename

    random.shuffle(flashcards) #shuffling so it's better for review

    print("\n" + "="*50)
    print(f"Loaded deck: {file_name}")
    print(f"Total cards available: {len(flashcards)}")
    print ("Let the review begin!")
    print("="*50 + "\n")

    while True: #using this allows to keep going on until user provide valid number
        num_q = input(f"There are {len(flashcards)} cards. How many would you like? ")
        if not num_q.isdigit(): #make sure the user is typing numbers, and not other stuff
            print("Please type a NUMBER.")
            continue
        num_q = int(num_q)
        if 1 <= num_q <= len(flashcards): #if number is not in the range, it'll request a redo
            break
        print(f"Please type a number between 1 and {len(flashcards)}.")
    print("Okay! We'll do", num_q, "question(s).")

    score = 0
    for i in range(num_q):#repeat for the number of questions the user requested
        term, definition = flashcards[i]
        user_text = (
            f"Q{i+1}. What is the name of the element with symbol '{term}'? "
            "(type 'quit' to end early) "
        )
        answer = input(user_text).strip().lower()

        if answer == "quit": #allows user to quit and save progress 
            print(f"Quitting early… saving score so far: {score}/{i}")
            final_score = score
            question_total = i  # counts completed questions only
            return -1

        if answer == definition.lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {definition}\n")

    print("-"*36)
    print(f"Your score: {score}/{num_q}")
    print("-"*36 + "\n")

    #store results so add_scores() can write to the history file
    final_score = score
    question_total = num_q

    return score


def show_scores():
    print("\n=== Previous Scores ===")
    #prevent from crashing if there are no files
    try:
        with open("scores.txt", "r") as score_file:
            lines = score_file.readlines()
    except FileNotFoundError:
        print("No scores file found yet. Let's start playing the game!")
        return

    printed = False
    #skip blank lines to make output clean
    for line in lines:
        text = line.strip()
        if text:
            print(text)
            printed = True
    if not printed:
        print("No scores recorded yet.")


def add_scores():
    global final_score, question_total, file_name
    username = ""
    while username.strip() == "":
        username = input("Enter your name: ").strip()
        if username == "":
            print("Please enter a non-empty name.")
    now = time.ctime()
    record = f"{username} ; {final_score}/{question_total} ; {file_name} ; {now}\n"
    try:
        with open("scores.txt", "a") as score_file:
            score_file.write(record)
        print("✅ Score saved!")
    except OSError as e:
        print("❌ Could not write to file:", e)
        

def print_error():
    print("*" * 50)
    print(" " * 22 + "error!" + " " * 22)
    print(" " * 12 + "that is not a valid option" + " " * 12)
    print(" " * 17 + "please try again" + " " * 17)
    print("*" * 50)


def main():
    # Menu options
    initial_choices = ["play", "see history", "exit"]
    file_types = [".txt", ".csv", "txt", "csv"]
    p_options = ["play", "p", "play game"]
    h_options = ["see history", "history", "h", "see", "sh", "s"]
    e_options = ["exit", "e", "exit game"]

    first_choice = ""
    game_on = True

    while game_on:
        print(" \nHello User! Welcome to the Ultimate Chemistry Periodic Table Review Game!")
        time.sleep(1)
        print("Let's get started!")
        while first_choice not in e_options:
            for item in initial_choices:#show menu options every time so user knows choices
                print(f"- {item}")
            first_choice = input("what would you like to do?\n> ").lower().strip()

            if first_choice in p_options:
                quiz_fn = input("what is the name of your file? (periodic_table)\n> ").lower().strip()
                quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                while quiz_ext not in file_types: #make sure file type is txt/csv
                    print_error()
                    print("your choices are:")
                    for item in file_types:
                        print(f"- {item}")
                    quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                file_url = quiz_fn + (".csv" if quiz_ext in [".csv", "csv"] else ".txt")

                result = play_quiz(file_url)

                # If quiz couldn't start (bad file / empty deck): do not save
                if result is None:
                    continue

                # Early quit: save partial and exit program
                if result == -1:
                    if question_total > 0: #avoid 0/0 if quitting immediately
                        add_scores()
                    print("Returning to menu...\n")
                    first_choice = "" 
                    continue
                # Normal completion: save and show menu again
                if question_total > 0:
                    add_scores()
                first_choice = "" #reset choice
                continue     #return to menu

            elif first_choice in h_options:
                show_scores()

            elif first_choice in e_options:
                game_on = False

            else:
                print_error()

        print("goodbye!")


if __name__ == "__main__":
    main()