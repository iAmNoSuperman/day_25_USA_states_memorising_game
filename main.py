import turtle
import pandas

ALIGNMENT = 'Center'
FONT = ('Courier', 10, 'normal')
MOVE = False


def refresh_new_best_score(current_score, best_score):  # at the end of the game we:
    if current_score > best_score:  # save new high score into the file,
        best_score = current_score  # reset the current score
        with open("data.txt", mode="w") as file:  # and update the scoreboard =)
            file.write(f"{best_score}")


def download_high_score():  # this download (if possible) previous high score =)
    with open("data.txt", mode="r") as save_data:
        return int(save_data.read())


# TODO This is a game of memorising all 50 states of USA.
#  It analyses the csv file with states and their whereabouts
#  (as x and y coordinates) on the background image
#  If user guess is correct, the name of the state then pop on
#  it's corresponding position on the screen.
#  Else, the game will continue till all the states are found
#  or the user chooses to quit.

main_screen = turtle.Screen()
image = "blank_states_img.gif"
main_screen.title("USA State's game!")
main_screen.addshape(image)
turtle.shape(image)
state_writer = turtle.Turtle()
state_writer.hideturtle()
state_writer.penup()
list_of_guessed_states = []
score = 0
high_score = download_high_score()

data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()

game_is_on = True
while game_is_on:
    user_guess = main_screen.textinput(title=f"Guess the State! Best score:{high_score}/50",
                                       prompt="What's another state's name?")
    user_guess = user_guess.title()

    if user_guess in all_states:
        if user_guess not in list_of_guessed_states:
            right_answer = data[data.state == user_guess]
            text = str(right_answer.state)
            list_of_guessed_states.append(text)
            score += 1
            state_writer.goto(int(right_answer.x), int(right_answer.y))
            state_writer.write(user_guess, MOVE, ALIGNMENT, FONT)
    if user_guess.title() == "Exit":
        refresh_new_best_score(score, high_score)
        game_is_on = False

refresh_new_best_score(score, high_score)
main_screen.exitonclick()

# Save the best score into a new file or rewritting it:

# TODO In case you need to find coordinates of clicked point
# def get_mouse_click_coor(x, y):
#     print(x, y)
#
# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()
