import time #record the time to save score
import random #shuffle the flashcards
final_score = 0 
question_total = 0
file_name = ""


def play_quiz(filename):
    print(f"play_quiz function called with {filename}")
    try: 
        file = open(filename, "r")
    except FileNotFoundError:
        print ("file not found, please check your spelling and try again")
        return 0
    lines = file.readlines()  
    file.close() 
    print("Number of lines:", len(lines))
    if len(lines)> 0:
        print ("The First line is:", lines [0].strip())
    return 0

    flashcards = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue


def show_scores():
    print("shows_scores function called")

    

def add_scores():
    print("add_scores function called")


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
        print("welcome to the review game")
        
        while first_choice not in e_options: #first runs bc first_choice == "", then bc they haven't said exit
            for item in initial_choices: #prints out play, see history, and exit
                print(f"- {item}")
            first_choice = input("what would you like to do?\n> ").lower().strip()
            if first_choice in p_options: #playing the game
                quiz_fn = input("what is the name of your file?\n> ").lower().strip()
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