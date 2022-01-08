from pesel_functions import *
def main():
    try:
        population = int(input('Enter number of citizens (positive integer): '))
        if population <= 0:
            population = randint(5,20)
            print(f"Your input wasn't a positive integer (input>0). Population was randomly generated to be: {population}")
        citizens = Society(population)
    except ValueError:
        citizens = Society(randint(5,20))
        print(f"You input for number of citizens wasn't a number. We randomly generated size of society for you: {citizens.count_population()}")
    while True:
        action = input('''\nWhat do you want to do:
        1 add_citizen  | 2 delete_citizen   | 3 change_pesel
        4 show_society | 5 count_population | 6 count_man
        7 count_woman  | 8 citizen_info     | 9 terminate_program
        Command: ''')
        print('\n')
        if action == '1' or action == 'add_citizen':
            citizens.add_citizen()
            print(f'''citizen was added:\n{citizens.society_dataframe()[['name','pesel']].iloc[citizens.count_population()-1].to_string()}''')
        elif action == '2' or action == 'delete_citizen':
            print(citizens)
            to_delete = int(input('Which citizen do you want to delete from society?(Enter index) '))
            citizen_delete = citizens.society_dataframe().drop("indieces",axis=1).loc[to_delete-1].to_string()
            citizens.ban_citizen(to_delete)
            print(f'\nCitizen has been deleated:\n{citizen_delete}')
        elif action == '3' or action == 'change_pesel':
            print(citizens)
            index = int(input("Which person's pesel do you want to change?(Enter index) "))
            old = citizens.society_dataframe().at[index-1,'pesel']
            new = input('What is your desired new pesel? ')
            citizens.change_pesel(index,new)
            print(f"{citizens.society_dataframe().at[index-1,'name']}'s pesel changed.\n old: {old}\n new: {new}")
        elif action == '4' or action == 'show_society':
            print(citizens)
        elif action == '5' or action == 'count_population':
            print(f"Society's population right now is: {citizens.count_population()}")
        elif action == '6' or action == 'count_man':
            print(f"Number of males in society: {citizens.count_man()}.")
        elif action == '7' or action == 'count_woman':
            print(f"Number of females in society: {citizens.count_woman()}.")
        elif action == '8' or action == 'citizen_info':
            print(citizens)
            to_show = int(input('Enter index of a citizen to show: '))
            print('\n',citizens.get_info(to_show))
        elif action == '9' or action == 'terminate_program':
            print('Program terminated.')
            break

if __name__ == '__main__':
    main()
