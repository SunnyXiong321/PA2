'''
Make a flashcard review game that reads through a file
where each line consists of a term and its definition.

An example text file and an example CSV file have been provided to you.

A masterful program includes the ability to create a new file
and load your own terms/definitions into it, before running the quiz on that file.

Save game records to a different file. Log username and high score.
Allow the user the option to view this file by printing it to the console.

You should at minimum edit the helper functions.
You may not necessarily have to edit the main function.
'''

def play_quiz(filename):
    print(f"play_quiz function called with {filename}")


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
        
        while first_choice not in e_options:
            for item in initial_choices:
                print(f"- {item}")
            first_choice = input("what would you like to do?\n> ").lower().strip()
            if first_choice in p_options:
                quiz_fn = input("what is the name of your file?\n> ").lower().strip()
                quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                while quiz_ext not in file_types:
                    print_error()
                    print("your choices are:")
                    for item in file_types:
                        print(f"- {item}")
                    quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                if quiz_ext in [".csv","csv"]:
                    file_url = quiz_fn+".csv"
                else:
                    file_url = quiz_fn+".txt"
                play_quiz(file_url)
                add_scores()
            elif first_choice in h_options:
                show_scores()
            elif first_choice in e_options:
                game_on = False
            else:
                print_error()
        
        print("goodbye!")

main()