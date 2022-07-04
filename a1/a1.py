"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""
import random
import sys
from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)

# Replace these <strings> with your name, student number and email address.
__author__ = "<Yanran LI>, <47224696>"
__email__ = "<yanran.li1@uqconnect.edu.au>"


# Add your functions here
def has_won(guess: str, answer: str) -> bool:
    """Returns True if the guess matches answer exactly.

    Parameters:
        guess(str):The name of guess enter.
        answer(str):The name of right answer.

    Returns:
        bool:Distinguish whether matches.
    """
    # Precondition: they have same length
    if guess == answer:
        return True
    else:
        return False

def has_lost(guess_number: int) -> bool:
    """Returns True if the number of guess greater or equal than 6.

    Parameters:
        guess_number(int):number of guesses.

    Returns:
        bool:Distinguish the number result.
    """
    if guess_number >= 6:
        return True
    else:
        return False

def remove_word(words: tuple[str, ...], word: str) -> tuple[str, ...]:
    """Returns a copy of words with word removed.

    Parameters:
        words(tuple):A tuple containing all the words in the file.
        word(str):A word needed to be deleted.

    Returns:
        tuple<str>: A new tuple which removed word.
    """
    if word in words:
        index_num = words.index(word)
        new_words = words[:index_num] + words[index_num + 1:]
        return new_words

def prompt_user(guess_number: int, words: tuple[str, ...]) -> str:
    """
    Prompts the user for the next guess.

    Parameters:
        guess_number: the time of guess.
        words: the word which is existing.
    Returns:
        Return str contains 1.right/2.'invalid'/3.'help'
    """
    while True:
        re_guess = input("Enter guess " + str(guess_number) + ": ").lower()
        if len(re_guess) == 6:
            if re_guess in words:
                return re_guess
            else:
                print("Invalid! Unknown word")
                continue
        elif re_guess == 'k':
            return 'k'
        elif re_guess == 'q':
            return 'q'
        elif re_guess == 'h':
            return 'h'
        elif re_guess == 'y':
            return 'y'
        elif re_guess == 'a':
            return 'a'
        else:
            print("Invalid! Guess must be of length 6")
            continue

def process_guess(guess: str, answer: str) -> str:
    """Returns a modified representation of guess

    Parameters:
        guess(str):a string of guess input
        answer(str):the right answer which need to be verity

    Returns:
        str:Return a line of guess
    """
    guess_graph = []
    count = 0
    for i in range(len(guess)):
        if guess[i] not in guess[0:count]:
            if guess[i] in answer:
                if guess[i] == answer[i]:
                    guess_graph += CORRECT
                else:
                    guess_graph += MISPLACED
            else:
                guess_graph += INCORRECT
        else:
            index_repeat_list = []
            if guess[i] in answer:
                for j in range(6):
                    if guess[j] == guess[i]:
                        index_repeat_list.append(j)
                for j in index_repeat_list:
                    if guess[j] == answer[j]:
                        guess_graph += CORRECT
                        index_repeat_list.remove(j)
                        for n in index_repeat_list:
                            guess_graph[n] = INCORRECT
                    else:
                        guess_graph += MISPLACED
                        index_repeat_list.remove(j)
                        print(index_repeat_list)
                        for n in index_repeat_list:
                            guess_graph[n] = INCORRECT
            else:
                guess_graph += INCORRECT
        count = count+1

    return ''.join(guess_graph)
    # print("\n")

def update_history(history: tuple[tuple[str, str], ...], guess: str, answer: str) -> tuple[tuple[str, str], ...]:
    """Returns a copy of history updated to include the latest guess

    Parameters:
        history(tuple):a tuple used to stored (guess,result)
        guess(str):the user input
        answer(str):the real result

    Returns:
        tuple:the new tuple which contain latest guess.
    """
    if not history:
        history = (guess, process_guess(guess, answer))
        new_history = (history,)
    else:
        add_tuple = (guess, process_guess(guess, answer))
        new_history = history + (add_tuple,)
    return new_history

def print_history(history: tuple[tuple[str, str], ...]) -> None:
    """
    Print the guess history
    Parameters:
        history: received the history tuple
    Returns:
        no return,just print
    """
    print("---------------")
    count_history = int(len(history))
    #print(count_history)
    i = 0
    while i < count_history:
        print("Guess " + str(i + 1) + ": ", end=' ')
        j = 0
        while j < 2:
            if j == 0:
                guess_list = list(history[i][j])
                # i = int(i)
                guess_str = " ".join(guess_list)
                print(guess_str)
            else:
                #print("         " + history[i][j])
                print("         ", end='')
                if True:
                    guess_list = list(history[i][j])
                    # i = int(i)
                    guess_str = "".join(guess_list)
                    print(guess_str)
            j += 1
        i += 1
        print("---------------")
    print("")

def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    """
    This function used to print the information about each letter
    Parameters:
        history: received the history tuple
    Returns:
        no return,just print
    """
    print("\nKeyboard information")
    print("------------")
    guess_str = str(history)
    Alphabet = "a@b.c@d.e@f.g@h.i@j.k@l.m@n.o@p.q@r.s@t.u@v.w@x.y@z."
    for each in Alphabet:
        if each in guess_str:
            j = guess_str.index(each)
            if guess_str.count(each) < 2:
                print(each + ": " + guess_str[j + 10], end='')
            else:
                guess_str_slice = guess_str[j + 1:]
                i = guess_str_slice.index(each)
                if guess_str[j + 10] == guess_str_slice[i + 10]:
                    print(each + ": " + guess_str_slice[i + 10], end='')
                elif (guess_str_slice[i + 10] == CORRECT)or(guess_str[j + 10] == CORRECT):
                    print(each + ": " + CORRECT, end='')
                elif (guess_str_slice[i + 10] == MISPLACED)or(guess_str[j + 10] == MISPLACED):
                    print(each + ": " + MISPLACED, end='')
                else:
                    print(each + ": " + INCORRECT, end='')
        elif each == ".":
            print("")
        elif each == "@":
            print("\t",end='')
        else:
            print(each + ":  ", end='')
    print("")

def print_stats(stats: tuple[int, ...]) -> None:
    """
    prints the stats in a user-friendly way.

    Parameters:
        stats: The tuple contains completed times to finish games.
    Returns:
        None
    """
    print("\nGames won in:")
    for i in range(1,8):
        if i != 7:
            print(str(i), "moves:", str(stats[i-1]))
        else:
            print("Games lost:", str(stats[i-1]))

def win_result(stats: tuple[int, ...],count_num) -> tuple[tuple[str, str], ...]:
    """
    prints the win information
    Parameters:
        stats: The tuple contains completed times to finish games.
        count_num: The sequence of success
    Returns:
        return the times tuple
    """
    times_list = list(stats)
    times_list[count_num - 1] = str(int(times_list[count_num - 1]) + 1)
    times_tuple = tuple(times_list)
    print("Correct! You won in " + str(count_num) +" guesses!")
    print_stats(times_tuple)
    return times_tuple

def lose_result(stats: tuple[int, ...],answer) -> tuple[tuple[str, str], ...]:
    """
    prints the lose information
    Parameters:
        stats: The tuple contains completed times to finish games.
        count_num: The sequence of fail
    Returns:
        return the times tuple
    """
    times_list = list(stats)
    times_list[6] = str(int(times_list[6]) + 1)
    times_tuple = tuple(times_list)
    print("You lose! The answer was: " + answer)
    print_stats(times_tuple)
    return times_tuple

def game_next() -> str:
    """
    Ask the user if they want to play the game again
    Return:
        return user's answer
    """
    answer = input("Would you like to play again (y/n)? ").lower()
    return answer

def guess_next(vocal: tuple[str,...], history: tuple[tuple[tuple[str,str]],...]) -> Optional[str]:
    """
        help user to guess the next word
        Parameters:
            vocal: The tuple contains words.
            history: received the history tuple
        Returns:
            return the word which satisfied the need
    """
    guess_list = list(history)
    word_last = list(vocal)
    for each in guess_list:
        index_correct_list = []
        char_correct_list = []
        index_misplaced_list = []
        char_misplaced_list = []
        index_incorrect_list = []
        char_incorrect_list = []

        for j in range(len(each[1])):
            if each[1][j] == CORRECT:
                index_correct_list.append(j)
            elif each[1][j] == MISPLACED:
                index_misplaced_list.append(j)
            elif each[1][j] == INCORRECT:
                index_incorrect_list.append(j)

        if index_incorrect_list:
            for j in index_incorrect_list:
                char_incorrect_list.append(each[0][j])
        if index_correct_list:
            for j in index_correct_list:
                char_correct_list.append(each[0][j])
        if index_misplaced_list:
            for j in index_misplaced_list:
                char_misplaced_list.append(each[0][j])

        for i in char_incorrect_list:
            count = len(word_last)
            bek = []
            for j in range(count):
                if i in word_last[j]:
                    bek.append(j)
            word_last = [word_last[j] for j in range(count) if (j not in bek)]

        for i in range(len(char_correct_list)):
            index = index_correct_list[i]
            count = len(word_last)
            bek = []
            for j in range(count):
                if char_correct_list[i] != word_last[j][index]:
                    bek.append(j)
            word_last = [word_last[j] for j in range(count) if (j not in bek)]

        for i in range(len(char_misplaced_list)):
            count = len(word_last)
            index = index_misplaced_list[i]
            bek = []
            for j in range(count):
                if (char_misplaced_list[i] not in word_last[j]) or \
                        (char_misplaced_list[i] == word_last[j][index]):
                    bek.append(j)
            word_last = [word_last[j] for j in range(count) if (j not in bek)]

    if len(word_last) == 0:
        str_return = None
    elif len(word_last) == 1:
        str_return = word_last[0]
    else:
        index_random = random.randint(0, len(word_last) - 1)
        str_return = word_last[index_random]

    return str_return

def main():
    times_tuple = (0, 0, 0, 0, 0, 0, 0)  # times
    words = load_words(ANSWERS_FILE)
    lists = load_words(VOCAB_FILE)
    exit_flag = False
    while True:
        answer_right = choose_word(words)
        record_tuple = ()# history
        count = 0

        while not has_lost(count):
            guess_str = prompt_user(count+1,lists)
            if len(guess_str) == 6:
                record_tuple = update_history(record_tuple,guess_str,answer_right)
                print_history(record_tuple)
                count += 1
                if has_won(guess_str,answer_right):
                    remove_word(words, answer_right)
                    times_tuple = win_result(times_tuple,count)
                    break
            elif guess_str == 'k':
                print_keyboard(record_tuple)
            elif guess_str == 'q':
                exit_flag = True
                break
            elif guess_str == 'h':
                print("Ah, you need help? Unfortunate.")
            elif guess_str == 'a':
                guess_auto = guess_next(words,record_tuple)
                record_tuple = update_history(record_tuple, guess_auto, answer_right)
                print_history(record_tuple)
                count += 1
                if has_won(guess_auto, answer_right):
                    remove_word(words, answer_right)
                    times_tuple = win_result(times_tuple, count)
                    break
            elif guess_str == 'y':
                break
            else:
                continue

        if exit_flag == True:
            break

        while has_lost(count):
            lose_result(times_tuple,answer_right)
            break

        if guess_str !='y':
            if game_next() == 'y':
                continue
            else:
                break

if __name__ == "__main__":
    main()