import csv
import random

music = [(("Pink Floyd", "The Dark Side Of The Moon"), (1973, "psychodelic rock", "43:00")),
         (("Britney Spears", "Baby One More Time"), (1999, "pop", "42:20"))]

red = "\033[1;31m"
off = "\033[0;0m"
darkyellow = "\033[0;33m"
blue = "\033[1;34m"
####----------------------------------------------------------------------------------------------------------------####
def handle_new_album_data():
    new_album_data = []
    storage = []

    questions = [
    "What is the name of the author?: ",
    "What is the title of this album?: ",
    "When It was released(year)?: ",
    "What is the genre of this album?: ",
    "Tell me the length of this recording((len(MM)>0 and len(SS) = 2 | MM:SS): "
    ]


    for question in questions:
        if question == "When It was released(year)?: ":
            ask_for_data = check_is_number(question)
        elif question == questions[4]:
            ask_for_data = check_is_right_formatted_time(question)  # MM:SS
        else:
            ask_for_data = input(question).title()

        new_album_data.append(ask_for_data)

    storage = ((new_album_data[0], new_album_data[1]), (new_album_data[2], new_album_data[3], new_album_data[4]))

    return storage
####----------------------------------------------------------------------------------------------------------------####
def check_is_number(question=""):

    ask_for_number = ""
    while ask_for_number.isdigit() == False:
        ask_for_number = input(question)

        if ask_for_number.isdigit() == False:
            print(red + "It's not a number!" + off)

    return ask_for_number
####----------------------------------------------------------------------------------------------------------------####
def check_is_right_formatted_time(question="",):

    length_of_recording = ""
    funny_story = True
    k = ""
    while funny_story:
        length_of_recording = input(question)
        if ":" in length_of_recording:
            for i in range(len(length_of_recording)):
                if ':' in length_of_recording[i]:
                    k = i

            if length_of_recording[:k].isdigit() and length_of_recording[k+1:].isdigit():
                if len(length_of_recording[k+1:]) == 2:
                    print("very good")
                    funny_story = False
                else:
                    print(darkyellow + "Something goes wrong!" + off)
            else:
                print(darkyellow + "Something goes wrong!" + off)
        else:
            print(darkyellow + "Something goes wrong!" + off)

    return length_of_recording
####----------------------------------------------------------------------------------------------------------------####
def option_list():
    print("""
Welcome in the CoolMusic! Choose the action:
     1) Add new album
     2) Finding
     3) Calculate the age of all albums
     4) Choose a random album by genre
     5) Show the amount of albums by an artist
     6) Find the longest-time album
     0) Exit
         """)

####----------------------------------------------------------------------------------------------------------------####
def open_data_file():

    bugged_data = []
    data_converter = []
    with open('music.csv', 'r') as csvfile:
        infoReader = csv.reader(csvfile)

        for i in infoReader:
            data_converter.append(i)

        for i in range(len(data_converter)):

            one_level_less = data_converter[i][0].split(" | ")
            data_converter[i] = one_level_less
            if "\ufeff" in data_converter[i][0]:
                data_converter[i][0] = data_converter[i][0].replace("\ufeff", "")


        index_n_back = 0
        for i in range(len(data_converter)):  ## Handling some basic bugs
            if len(data_converter[i - index_n_back]) != 5:

                bugged_data.append(data_converter[i - index_n_back])
                data_converter.remove(data_converter[i - index_n_back])
                index_n_back += 1
            if not data_converter[i - index_n_back][2].isdigit():
                bugged_data.append(data_converter[i - index_n_back])
                data_converter.remove(data_converter[i - index_n_back])
                index_n_back += 1
            if ":" not in data_converter[i - index_n_back][4]:
                bugged_data.append(data_converter[i - index_n_back])
                data_converter.remove(data_converter[i - index_n_back])
                index_n_back += 1
            ind = data_converter[i - index_n_back][4].index(":")  # index of double_point in time section
            if data_converter[i - index_n_back][4][:ind].isdigit() == False or data_converter[i - index_n_back][4][ind+1:].isdigit() == False or len(data_converter[i - index_n_back][4][ind+1:]) > 2:
                bugged_data.append(data_converter[i - index_n_back])
                data_converter.remove(data_converter[i - index_n_back])
                index_n_back += 1
            if int(data_converter[i - index_n_back][4][ind+1:]) > 59:
                bugged_data.append(data_converter[i - index_n_back])
                data_converter.remove(data_converter[i - index_n_back])
                index_n_back += 1


        if len(bugged_data) > 0:
            print("Dear user, I have found few or more bugged data formats.")
            print(blue + "But don't worry, we will delete them when you turn off and on again: " + off)
            amount_of_errors = 0
            for item in bugged_data:
                amount_of_errors += 1
                print("bugged output:",item)
            print("Amount of errors:", amount_of_errors)

        albums = []
        for x in range(len(data_converter)):
            albums += [((data_converter[x][0].title(),
                        data_converter[x][1].title()),
                        (data_converter[x][2],
                        data_converter[x][3].title(),
                        data_converter[x][4]))]

    return albums

####----------------------------------------------------------------------------------------------------------------####
def data_save(data):

    storage = []

    for i in range(len(data)):

        save_data = data[i][0][0] + " | " + data[i][0][1] + " | " + str(data[i][1][0]) + " | " + data[i][1][1] + " | " + data[i][1][2]
        storage.append(save_data)

    with open('music.csv', 'w') as csvfile:
        infoWriter = csv.writer(csvfile)

        for element in storage:
            infoWriter.writerow([element])
####----------------------------------------------------------------------------------------------------------------####
def finding_func():

    questions = [
    "Artist name: ",
    "Year of release: ",
    "Album name: ",
    "Letter(s): ",
    "Genre: "
    ]

    exploring_options = ""
    while exploring_options not in ["1","2","3","4","5"]:
        print("""
         1) Find albums by artist
         2) Find albums by year
         3) Find musician by album
         4) Find albums by letter(s)
         5) Find albums by genre
         """)
        exploring_options = input("What type of finding do you want to use?: ")
    storage = []
    index_values = []

    data_explorer = input(questions[int(exploring_options) - 1])
    if not data_explorer.isdigit() and str(exploring_options) in ["1", "2", "3", "5"]:
        data_explorer = data_explorer.title()

    if exploring_options == "4" and not data_explorer.isdigit():
        data_explorer = data_explorer.lower()

    if exploring_options in ["1","2","3", "4","5"]:
        if exploring_options == "1":
            index_values = [0,0,0,1]
        elif exploring_options == "2":
            index_values = [1, 0, 0, 1]
        elif exploring_options == "3":
            index_values = [0, 1, 0, 0]
        elif exploring_options == "4":
            index_values = [0, 1, 0, 1]
        elif exploring_options == "5":
            index_values = [1, 1, 0, 1]
        for x in range(len(list_of_albums)):
            if exploring_options == "4":
                if data_explorer in list_of_albums[x][index_values[0]][index_values[1]].lower():
                    storage.append(list_of_albums[x][index_values[2]][index_values[3]])
            else:
                if data_explorer == list_of_albums[x][index_values[0]][index_values[1]]:
                    storage.append(list_of_albums[x][index_values[2]][index_values[3]])

        if len(storage) > 0:
            for item in storage:
                print(item)
        else:
            print("You found!! NOTHING :D")

####----------------------------------------------------------------------------------------------------------------####
finish = True

list_of_albums = []
try:
    list_of_albums = open_data_file()
except:
    print(darkyellow + "Probably music.csv file doesn't exist" + off)
    print("Turn on again this software :)")
    open("music.csv", 'w').close()
    finish = False

while finish:
    option_list()

    right_input = ""
    while right_input != "I am number":
        num_input = input("What do you want to do ?: ")

        if num_input.isdigit() == False:
            print(red + "Please try again and put a digit or a number.\n" + off)
        else:
            right_input = "I am number"

    num_input = int(num_input)
####----------------------------------------------------------------------------------------------------------------####

    if num_input == 1:
        list_of_albums.append(handle_new_album_data())
####----------------------------------------------------------------------------------------------------------------####
    if num_input == 2:
        finding_func()
####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 3:
        sum_age = 0
        for i in range(len(list_of_albums)):
            sum_age += int(list_of_albums[i][1][0])
        print("Sum age of all albums:", sum_age)
####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 4:
        genre_storage = []
        for i in range(len(list_of_albums)):
            genre_storage.append(list_of_albums[i][1][1])
        print("Random album by genre: ", random.choice(genre_storage))
####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 5:

        artist_storage = []

        for i in range(len(list_of_albums)):
            if list_of_albums[i][0][0] not in artist_storage:
                artist_storage.append(list_of_albums[i][0][0])

        for artist in artist_storage:
            albums_by_artist_amount = 0

            for i in range(len(list_of_albums)):
                if artist == list_of_albums[i][0][0]:
                    albums_by_artist_amount += 1

            print(artist,"have",albums_by_artist_amount, end="")
            if albums_by_artist_amount == 0 or albums_by_artist_amount > 1:
                print(" albums.")
            else:
                print(" album.")
####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 6:
        time_album_storage = []

        for x in range(len(list_of_albums)):
            time_album_storage.append([list_of_albums[x][1][2],list_of_albums[x][0][1]])

        time_album_storage.sort(reverse=True)
        print("Longest length of recording:",time_album_storage[0][0],"Album:",time_album_storage[0][1])

    elif num_input == 0:

        finish = False
        data_save(list_of_albums)
