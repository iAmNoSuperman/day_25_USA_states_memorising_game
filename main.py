import turtle
import pandas

ALIGNMENT = 'Center'
FONT = ('Courier', 10, 'normal')
MOVE = False


def refresh_new_best_score(current_score, best_score):  # at the end of the game we:
    if current_score > best_score:                      # save new high score into the file,
        best_score = current_score                      # reset the current score
        with open("data.txt", mode="w") as file:        # and update the scoreboard =)
            file.write(f"{best_score}")


def download_high_score():                              # this download (if possible) previous high score =)
    with open("data.txt", mode="r") as save_data:
        return int(save_data.read())


# This is a game of memorising all 50 states of USA.
#  It analyses the csv file with states and their whereabouts
#  (as x and y coordinates) on the background image
#  If user guess is correct, the name of the state then pop on
#  it's corresponding position on the screen.
#  And behind the screen the game will save already guessed state
#  in a list of already guessed states and +1 the score.
#  Else, the game will continue till all the states are found
#  or the user chooses to quit.

# 1. configure the:
#   screen with an image background of a USA states map.
main_screen = turtle.Screen()
image = "blank_states_img.gif"
main_screen.title("USA State's game!")
main_screen.addshape(image)
turtle.shape(image)
#   turtle pen that put name of guessed state on its coordinates on the image of the map
state_writer = turtle.Turtle()
state_writer.hideturtle()
state_writer.penup()
#   a list for guessed states which is also a point to end of a game as its len reaches 50
list_of_guessed_states = []
#   a variable for a current score and downloaded previous high score
score = 0
high_score = download_high_score()
#   a data of all states with correscponded coordinates from a csv file, and create a list of state names out of it
data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()

# 2.While user hasn't guessed all the states we prompt they to guess another one
while len(list_of_guessed_states) < 50:
    user_guess = main_screen.textinput(title=f"{score}/50 States correct. Best score:{high_score}/50",
                                       prompt="What's another state's name?").title()
    if user_guess == "Exit":
        break
    if user_guess in all_states:
        if user_guess not in list_of_guessed_states:
            right_answer = data[data.state == user_guess]
            list_of_guessed_states.append(user_guess)
            score += 1
            state_writer.goto(int(right_answer.x), int(right_answer.y))
            state_writer.write(user_guess, MOVE, ALIGNMENT, FONT)

# After the game ends we create a csv file with all never mentioned states
states_to_learn = {
    "state": [],
    "x": [],
    "y": []
}
for state in all_states:
    if state not in list_of_guessed_states:
        new_state = data[data.state == state]
        states_to_learn['state'].append(new_state.state.item())
        states_to_learn['x'].append(int(new_state.x))
        states_to_learn['y'].append(int(new_state.y))
result_df = pandas.DataFrame(states_to_learn)
result_df.to_csv("states_to_learn.csv")

# Save the best score into a new file or rewriting it:
refresh_new_best_score(score, high_score)
main_screen.exitonclick()
