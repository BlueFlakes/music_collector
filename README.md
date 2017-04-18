# music_collector
import csv
import random

music = [(("Pink Floyd", "The Dark Side Of The Moon"), (1973, "psychodelic rock", "43:00")),
         (("Britney Spears", "Baby One More Time"), (1999, "pop", "42:20"))]

red = "\033[1;31m"
off = "\033[0;0m"
darkyellow = "\033[0;33m"
blue = "\033[1;34m"

####----------------------------------------------------------------------------------------------------------------####


def option_list():
    print("""
Welcome in the CoolMusic! Choose the action:
     1) Add new album
     2) Find albums by artist
     3) Find albums by year
     4) Find musician by album
     5) Find albums by letter(s)
     6) Find albums by genre
     7) Calculate the age of all albums
     8) Choose a random album by genre
     9) Show the amount of albums by an artist
    10) Find the longest-time album
     0) Exit
         """)

####----------------------------------------------------------------------------------------------------------------####


def data_reader():

    try:
        data_converter = []
        with open('music.csv', 'r') as csvfile:
            infoReader = csv.reader(csvfile)

            for i in infoReader:
                data_converter.append(i)

            for i in range(len(data_converter)):

                one_level_less = data_converter[i][0].split(" | ")

                data_converter[i] = one_level_less

            global albums
            albums = []
            for x in range(len(data_converter)):

                albums += [((data_converter[x][0], data_converter[x][1]), (data_converter[x][2], data_converter[x][3], data_converter[x][4]))]
    except:
        open('music.csv', 'w').close()
        print("Music.csv doesn't exist !")

####----------------------------------------------------------------------------------------------------------------####


def data_save():

    storage = []

    for i in range(len(albums)):

        save_data = albums[i][0][0] + " | " + albums[i][0][1] + " | " + str(albums[i][1][0]) + " | " + albums[i][1][1] + " | " + albums[i][1][2]

        storage.append(save_data)

    with open('music.csv', 'w') as csvfile:
        infoWriter = csv.writer(csvfile)

        for element in storage:
            infoWriter.writerow([element])

####----------------------------------------------------------------------------------------------------------------####


def check_if_word(special_keys):
    '''
   |---------------------------------------------------------------------------|
   |The task of this function is to check if a string of words has been entered|
   |---------------------------------------------------------------------------|
    '''
    delete_space = ""
    while delete_space.isalpha() == False:

        #---------------------------------------------------------------------------------------------------------------
        if special_keys == "name":
            informations = input("What is the name of author?: ")
        elif special_keys == "album_name":
            informations = input("Disk title?: ")
        elif special_keys == "music_type":
            informations = input("What type of music is it?: ")
        elif special_keys == "artist":
            informations = input("Give me the name of artist: ")
        elif special_keys == "find_musician":
            informations = input("Tell me the name of the album: ")
        elif special_keys == "find_album_by_letters":
            informations = input("Letters to look for: ")
        elif special_keys == "find_album_by_genre":
            informations = input("In which genre you want to look for?: ")
        elif special_keys == "random_album_by_genre":
            informations = input("In which genre you want to look for?: ")
        #---------------------------------------------------------------------------------------------------------------
        delete_space = informations
        space_index = []

        for sign in range(len(informations)):  # get the index of this sign " "
            if informations[sign] == " ":
                space_index.append(sign)

        k = 0
        for spc_ind in space_index:  # delete space from string
                delete_space = delete_space[:spc_ind - k] + delete_space[spc_ind + 1 - k:]
                k += 1

        if delete_space.isalpha() == False:
            print(darkyellow + "Something goes wrong!\n" + off)

    return informations

####----------------------------------------------------------------------------------------------------------------####


def check_if_number(special_keys):

    k = 0
    while k != 1:
        if special_keys == "year":
            the_year = input("Release date: ")

        elif special_keys == "find_album":
            the_year = input("In which year you would like to search: ")

        if the_year.isdigit():
            k = 1
            return the_year
        else:
            print(darkyellow + "Something goes wrong!\n" + off)

####----------------------------------------------------------------------------------------------------------------####


def check_if_right_time_format():

    k = 0
    while k != 1:
        time = input("Length of recording in minutes and seconds(like this 43:20): ")

        indeks = 0
        for index in range(len(time)):
            if time[index] == ":":
                indeks = index
        if time[:indeks].isdigit() and time[indeks + 1:].isdigit() and time[indeks] == ":" and len(time) <= 5:

            if len(time[indeks + 1:]) < 2:
                time += "0"

            if int(time[:indeks]) < 61 and int(time[indeks + 1:]) < 60:

                if time[:indeks] == "60":
                    time = time[:indeks + 1] + "00"

                k = 1
                return time
            else:
                print(darkyellow + "Something goes wrong!\n" + off)

        else:
            print(darkyellow + "Something goes wrong!\n" + off)
####----------------------------------------------------------------------------------------------------------------####


data_reader()
finish = ""

while finish != "koniec":
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

        answer = []

        for key in ["name", "album_name", "release_date", "music_type", "time_format"]:

            if key in ["name", "album_name", "music_type"]:
                data = check_if_word(key).title()

            elif key == "release_date":
                data = check_if_number('year')

            elif key == "time_format":
                data = check_if_right_time_format()

            answer.append(data)

        print(answer)
        albums += [((answer[0], answer[1]), (answer[2], answer[3], answer[4]))]

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 2:

        find_album_by_artist = check_if_word('artist')
        storage = []
        k = 0
        for i in range(len(albums)):
            if find_album_by_artist.title() in albums[i][0][0]:
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print()
            print(find_album_by_artist.title() + " albums: ")
            for item in storage:
                print(item)

        else:
            print("Probably this artist doesn't exist.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 3:
        find_album_by_year = check_if_number('find_album')

        storage = []
        k = 0
        for i in range(len(albums)):
            if find_album_by_year in albums[i][1][0]:
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print()
            print(find_album_by_year + ":")
            for item in storage:
                print(item)

        else:
            print("There is no album there.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 4:
        find_musician_by_album = check_if_word('find_musician')

        for i in range(len(albums)):
            if find_musician_by_album.lower() in albums[i][0][1].lower():
                print(blue + "The author of " + find_musician_by_album.title() + " is " + albums[i][0][0] + off)

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 5:

        find_album_by_letters = check_if_word('find_album_by_letters')
        storage = []
        k = 0
        for i in range(len(albums)):
            if find_album_by_letters.lower() in albums[i][0][1].lower():
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print()
            print("You can find these letters in those albums: ")
            for item in storage:
                print(item)

        else:
            print("This letters doesn't exists in any album.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 6:

        find_album_by_genre = check_if_word('find_album_by_genre')
        storage = []
        k = 0
        for i in range(len(albums)):
            if find_album_by_genre.lower() in albums[i][1][1].lower():
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print()
            print("In this genre you can find those albums: ")
            for item in storage:
                print(item)

        else:
            print("Error, no albums there.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 7:

        sum_age = 0
        for i in range(len(albums)):
            sum_age += int(albums[i][1][0])
        print("Sum of all albums age:", sum_age)

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 8:

        random_album_by_genre = check_if_word('random_album_by_genre')
        storage = []
        k = 0
        for i in range(len(albums)):
            if random_album_by_genre.lower() in albums[i][1][1].lower():
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print(random.choice(storage))
        else:
            print("I found nothing there.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 9:

        find_album_by_artist = check_if_word('artist')
        storage = []
        k = 0
        for i in range(len(albums)):
            if find_album_by_artist.title() in albums[i][0][0]:
                storage.append(albums[i][0][1])
                k += 1
        if k > 0:
            print()
            print(find_album_by_artist.title(), "have", len(storage), end="")
            if len(storage) == 1:
                print(" album.")
            else:
                print(" albums.")
        else:
            print("Probably this author doesn't exist.")

####----------------------------------------------------------------------------------------------------------------####
    elif num_input == 10:

        storage = []
        for i in range(len(albums)):
            storage.append(albums[i][1][2])

        for i in range(len(storage)):
            storage[i] = storage[i].replace(":", "")
            storage[i] = int(storage[i])

        storage.sort(reverse=True)
        find_longest_time_album = str(storage[0])

        if len(find_longest_time_album) == 3:
            find_longest_time_album = find_longest_time_album[:1] + ":" + find_longest_time_album[1:]
        elif len(find_longest_time_album) == 4:
            find_longest_time_album = find_longest_time_album[:2] + ":" + find_longest_time_album[2:]

        for i in range(len(albums)):
            if find_longest_time_album in albums[i][1][2]:
                print("Najdłuższy album to: " + albums[i][0][1])

    elif num_input == 0:
        finish = "koniec"
        data_save()
