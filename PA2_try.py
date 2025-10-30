import time #record the time to save score
import random #shuffle the flashcards
final_score = 0 
question_total = 0
file_name = ""


def play_quiz(filename):
    global file_name, final_score, question_total
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found. Please check your spelling and try again.")
        return None

    print("Number of lines:", len(lines))
    if len(lines) > 0:
        print("The first raw line is:", lines[0].strip())


    flashcards = []
    for line in lines:
        line = line.strip()
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
        if term and definition:
            flashcards.append([term, definition])

    if len(flashcards) == 0:
        print("No valid flashcards found in this file.")
        return None


    global file_name
    file_name = filename

    print("First flashcard:", flashcards[0])
    print("Total cards:", len(flashcards))

    random.shuffle(flashcards)


    while True:
        num_q = input(f"There are {len(flashcards)} cards. How many would you like? ")
        if not num_q.isdigit():
            print("Please type a NUMBER.")
            continue
        num_q = int(num_q)
        if 1 <= num_q <= len(flashcards):
            break
        print(f"Please type a number between 1 and {len(flashcards)}.")
    print("Okay! We'll do", num_q, "question(s).")

    score = 0
    for i in range(num_q):
        term, definition = flashcards[i]
        user_text = (
            f"Q{i+1}. What is the name of the element with symbol '{term}'? "
            "(type 'quit' to end early) "
        )
        answer = input(user_text).strip().lower()

        if answer == "quit":
            print(f"Quitting early… saving score so far: {score}/{i}")
            global final_score, question_total
            final_score = score
            question_total = i  # counts completed questions only
            return -1

        if answer == definition.lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {definition}\n")

    print(f"Your score: {score}/{num_q}\n")

    final_score = score
    question_total = num_q

    return score


def show_scores():
    print("\n=== Previous Scores ===")
    try:
        with open("scores.txt", "r") as score_file:
            lines = score_file.readlines()
    except FileNotFoundError:
        print("No scores file found yet. Let's start playing the game!")
        return

    printed = False
    for line in lines:
        text = line.strip()
        if text:
            print(text)
            printed = True
    if not printed:
        print("No scores recorded yet.")


def add_scores():
    global final_score, question_total, file_name
    username = input("Enter your name: ")
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
            for item in initial_choices:
                print(f"- {item}")
            first_choice = input("what would you like to do?\n> ").lower().strip()

            if first_choice in p_options:
                quiz_fn = input("what is the name of your file? (periodic_table)\n> ").lower().strip()
                quiz_ext = input("is it a .txt or .csv file?\n> ").lower().strip()
                while quiz_ext not in file_types:
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