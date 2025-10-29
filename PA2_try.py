import time #record the time to save score
import random #shuffle the flashcards
final_score = 0 
question_total = 0
file_name = ""


def play_quiz(filename):
    global file_name
    file_name = filename

    try: 
        file = open(filename, "r")
    except FileNotFoundError:
        print("file not found, please check your spelling and try again")
        return 0


    lines = file.readlines()  
    file.close() 

    print("Number of lines:", len(lines))
    if len(lines) > 0:
        print("The First line is:", lines[0].strip())


    flashcards = []
    for line in lines:
        line = line.strip() # remove spaces and \n
        if line == "":
            continue
        if "," in line:
            term, definition = line.split(",", 1)
        elif " - " in line:
            term, definition = line.split(" - ", 1)
        else:
            continue

        term = term.strip()
        definition = definition.strip()
        flashcards.append([term, definition])

    if len(flashcards) == 0: 
        print("No valid flashcards found in this file.") 
        return 0
    
    print("First flashcard:", flashcards[0])
    print("Total cards:", len(flashcards))

    random.shuffle(flashcards)


    while True:   # loop until user gives valid input
        num_q = input(f"There are {len(flashcards)} cards. How many would you like? ")

        # check if it's a number
        if not num_q.isdigit():
            print("Please type a NUMBER.")
            continue   # go back to top of loop

        # turn text to number
        num_q = int(num_q)

        # check if number is in valid range
        if 1 <= num_q <= len(flashcards):
            break   # ✅ valid → exit loop
        else:
            print(f"Please type a number between 1 and {len(flashcards)}.")

    print("Okay! We'll do", num_q, "question(s).")



    score = 0

    for i in range(num_q):
        term = flashcards[i][0]
        definition = flashcards[i][1]

        user_text = f"Q{i+1}. What is the name of element with this symbol:'{term}'? "
        answer = input(user_text).strip().lower()

        if answer == definition.lower():
            print("✅ Correct!\n")
            score += 1
        #if answer == "exit":

        else:
            print(f"❌ Incorrect. Correct answer: {definition}\n")
        

        

    print(f"Your score: {score}/{num_q}\n")

    # remember results for add_scores()
    global final_score, question_total
    final_score = score
    question_total = num_q

    return score

def show_scores():
    print ("\n=== Previous Scores ===")

    try:
        score_file = open("scores.txt", "r")  # read mode
    except FileNotFoundError: 
        print("No scores file found yet. Let's start playing the game!") 
        return 
    
    lines = score_file.readlines()
    score_file.close()

    
    if len(lines) == 0:
        print("No scores recorded yet.")
        return

    for line in lines:
        print(line.strip())   # remove extra newline
 
    

def add_scores():
    print("add_scores function called")
    global final_score, question_total, file_name

    # ask user for name
    username = input("Enter your name: ")

    # get timestamp
    now = time.ctime()

    # prepare a string to write into file
    record = f"{username} ; {final_score}/{question_total} ; {file_name} ; {now}\n"

    # open file in APPEND mode → keeps previous data
    try:
        score_file = open("scores.txt", "a")
        score_file.write(record)
        score_file.close()
        print("✅ Score saved!")
    except:
        print("❌ Could not write to file.")


def print_error():
    print("*"*50)
    print(" "*22+"error!"+" "*22)
    print(" "*12+"that is not a valid option"+" "*12)
    print(" "*17+"please try again"+" "*17)
    print("*"*50)

def main():
    #initialize variables
    initial_choices = ["play","see history","exit"]
    file_types = [".txt", ".csv", "txt", "csv"]
    p_options = ["play","p","play game"]
    h_options = ["see history", "history", "h", "see", "sh", "s"]
    e_options = ["exit","e","exit game"]
    first_choice = ""
    game_on = True

    while game_on:
        print("Hello User! Welcome to the Ultimate Chemistry Periodic Table Review Game!")
        time.sleep (1)
        print("Let's get started!")
        while first_choice not in e_options: #first runs bc first_choice == "", then bc they haven't said exit
            for item in initial_choices: #prints out play, see history, and exit
                print(f"- {item}")
            first_choice = input("what would you like to do?\n> ").lower().strip()
            if first_choice in p_options: #playing the game
                quiz_fn = input("what is the name of your file? (periodic_table)\n> ").lower().strip()
                quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                while quiz_ext not in file_types: #if file type isn't txt/csv, there will be error
                    print_error()
                    print("your choices are:")
                    for item in file_types: #prints out txt and csv
                        print(f"- {item}")
                    quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                if quiz_ext in [".csv","csv"]:#comma seperated value file
                    file_url = quiz_fn+".csv"
                else:
                    file_url = quiz_fn+".txt" #text file
                play_quiz(file_url)
                add_scores()
            elif first_choice in h_options:#looking at previous scores
                show_scores()
            elif first_choice in e_options:#exiting
                game_on = False
            else: #print error
                print_error()
        
        print("goodbye!")

main()