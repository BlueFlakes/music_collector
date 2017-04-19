import csv
import random


red = "\033[1;31m"
off = "\033[0;0m"
darkyellow = "\033[0;33m"
blue = "\033[1;34m"

####----------------------------------------------------------------------------------------------------------------####
def handle_new_album_data():
    new_album_data = []
    temporary_storage = []

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

    temporary_storage = ((new_album_data[0], new_album_data[1]), (new_album_data[2], new_album_data[3], new_album_data[4]))

    return temporary_storage
####----------------------------------------------------------------------------------------------------------------####
def check_is_number(question):

    ask_for_number = ""
    while not ask_for_number.isdigit():
        ask_for_number = input(question)

        if not ask_for_number.isdigit():
            print(red + "It's not a number!" + off)

    return ask_for_number
####----------------------------------------------------------------------------------------------------------------####
def check_is_right_formatted_time(question):

    length_of_recording = ""
    format_filter_on = True
    colon_index = ""

    while format_filter_on:
        length_of_recording = input(question)
        if ":" in length_of_recording:
            for i in range(len(length_of_recording)):
                if ':' in length_of_recording[i]:
                    colon_index = i

            if length_of_recording[:colon_index].isdigit() and length_of_recording[colon_index+1:].isdigit():
                if len(length_of_recording[colon_index+1:]) == 2:
                    format_filter_on = False
                else:
                    print(darkyellow + "Something goes wrong!" + off)
            else:
                print(darkyellow + "Something goes wrong!" + off)
        else:
            print(darkyellow + "Something goes wrong!" + off)

    return length_of_recording
####----------------------------------------------------------------------------------------------------------------####
def show_option_list():
    print("""
Welcome in the CoolMusic! Choose the action:
     1) Add new album
     2) Finding
     3) Calculate the age of all albums
     4) Choose a random album by genre
     5) Show the amount of albums by an artist
     6) Find the longest-time album
     7) Exit
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
            if  (data_converter[i - index_n_back][4][:ind].isdigit() == False         ## Three line condition
                    or data_converter[i - index_n_back][4][ind+1:].isdigit() == False
                    or len(data_converter[i - index_n_back][4][ind+1:]) > 2):
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

    temporary_storage = []

    for i in range(len(data)):

        save_data = (data[i][0][0] + " | " + data[i][0][1] + " | " + str(data[i][1][0]) + " | " + data[i][1][1] + " | "
                    + data[i][1][2])
        temporary_storage.append(save_data)

    with open('music.csv', 'w') as csvfile:
        infoWriter = csv.writer(csvfile)

        for item in temporary_storage:
            infoWriter.writerow([item])
####----------------------------------------------------------------------------------------------------------------####
def finding_func():

    questions = [
    "Artist name: ",
    "Year of release: ",
    "Album name: ",
    "Letter(s): ",
    "Genre: "
    ]

    finding_option = ""
    while finding_option not in ["1","2","3","4","5"]:
        print("""
         1) Find albums by artist
         2) Find albums by year
         3) Find musician by album
         4) Find albums by letter(s)
         5) Find albums by genre
         """)
        finding_option = input("What type of finding do you want to use?: ")
    temporary_storage = []
    index_values = []

    data_explorer = input(questions[int(finding_option) - 1])
    if finding_option in ["1", "2", "3", "5"]:
        data_explorer = data_explorer.title()
    elif finding_option == "4":                 # for option 4 we need lower() because if we get string "Inside"
        data_explorer = data_explorer.lower()   # and if we put "ide" title() we get "Ide" which doesn't exist
                                                # in string "Inside"
    if finding_option in ["1","2","3", "4","5"]:
        if finding_option == "1":
            index_values = [0,0,0,1]
        elif finding_option == "2":
            index_values = [1, 0, 0, 1]
        elif finding_option == "3":
            index_values = [0, 1, 0, 0]
        elif finding_option == "4":
            index_values = [0, 1, 0, 1]
        elif finding_option == "5":
            index_values = [1, 1, 0, 1]
        for x in range(len(list_of_albums)):
            if finding_option == "4":
                if data_explorer in list_of_albums[x][index_values[0]][index_values[1]].lower():
                    temporary_storage.append(list_of_albums[x][index_values[2]][index_values[3]])
            else:
                if data_explorer == list_of_albums[x][index_values[0]][index_values[1]]:
                    temporary_storage.append(list_of_albums[x][index_values[2]][index_values[3]])

        if len(temporary_storage) > 0:
            for item in temporary_storage:
                print(item)
        else:
            print("You found!! NOTHING :D")

####----------------------------------------------------------------------------------------------------------------####
#------------------
   # Globals

finish = True
list_of_albums = []
#------------------
try:
    list_of_albums = open_data_file()
except:
    print(darkyellow + "Probably music.csv file doesn't exist" + off)
    print("Turn on again this software :)")
    open("music.csv", 'w').close()
    finish = False

while finish:
    show_option_list()

    numb_input = None
    while not numb_input:
        numb_input = input("What do you want to do ?: ")

        if not numb_input.isdigit():
            print(red + "Please try again and put a digit or a number.\n" + off)
            numb_input = None
        else:
            numb_input = int(numb_input)
            if numb_input not in [1,2,3,4,5,6,7]:
                print(darkyellow + "This option doesn't exist." + off)


####----------------------------------------------------------------------------------------------------------------####

    if numb_input == 1:
        list_of_albums.append(handle_new_album_data())
####----------------------------------------------------------------------------------------------------------------####
    if numb_input == 2:
        finding_func()
####----------------------------------------------------------------------------------------------------------------####
    elif numb_input == 3:

        if len(list_of_albums) > 0:
            sum_age = 0
            for i in range(len(list_of_albums)):
                sum_age += int(list_of_albums[i][1][0])
            print("Sum age of all albums:", sum_age)
        else:
            print("I could not find any record in database.")
####----------------------------------------------------------------------------------------------------------------####
    elif numb_input == 4:
        genre_storage = []
        if len(list_of_albums) > 0:
            for i in range(len(list_of_albums)):
                if list_of_albums[i][1][1] not in genre_storage:
                    genre_storage.append(list_of_albums[i][1][1])

            possible_albums = []
            choosen_genre = random.choice(genre_storage)
            for i in range(len(list_of_albums)):
                if choosen_genre == list_of_albums[i][1][1]:
                    possible_albums.append(list_of_albums[i][0][1])

            print("Random album by genre:", random.choice(possible_albums))
        else:
            print("I could not find any record in database.")

####----------------------------------------------------------------------------------------------------------------####
    elif numb_input == 5:

        artist_storage = []
        if len(list_of_albums) > 0:
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
        else:
            print("I could not find any record in database.")
####----------------------------------------------------------------------------------------------------------------####
    elif numb_input == 6:
        len_recording_and_album_storage = []
        length_of_recordings = []
        finding_winner = {}  #  Dictionary because can find winner by key without sorting
        if len(list_of_albums) > 0:
            for x in range(len(list_of_albums)):
                len_recording_and_album_storage.append([list_of_albums[x][1][2],list_of_albums[x][0][1]])

            for i in range(len(len_recording_and_album_storage)):
                len_recording_and_album_storage[i][0] = len_recording_and_album_storage[i][0].replace(":", "")

            for item in len_recording_and_album_storage:
                finding_winner[int(item[0])] = item[1]

            for item in len_recording_and_album_storage:
                length_of_recordings.append(int(item[0]))

            length_of_recordings.sort(reverse=True)
            print("The longest time of recording the album:", finding_winner[length_of_recordings[0]])
        else:
            print("I could not find any record in database.")

    elif numb_input == 7:
        finish = False
        data_save(list_of_albums)
