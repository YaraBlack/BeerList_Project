import json

beer_dict = { }

# Output

def show_dict():
    if len(beer_dict) == 0:
        print("Your list is empty.\n")
    else:
        for i in beer_dict:
            print( "Name:", i, "\n% of alcohol:", beer_dict[i]['alcho'],"\nIngredients:", beer_dict[i]['ingredients'], \
            "\nDescription:", beer_dict[i]['description'], "\n" )
            

# Input

def add_dict():
    name = input("Enter a name of beer: ")
    beer_dict[name] = {
        'alco' : input("Enter % of alcohol in beer: "),
        'ingredients' : input("Enter the beer's ingredients: "),
        'description' : input("Describe a beer: ")
    }
    print("\n")

# Delete an item

def remove_dict():
    ind = input("Enter the name of beer you want to remove: ")
    if ind in beer_dict.keys():
        del beer_dict[ind]
    print(ind, " has been successfully removed!\n")

# Write to file

def json_writing(Dict):
    fileW = open("Beer.json", "w", encoding = "utf-8")
    json.dump(Dict, fileW, ensure_ascii = False, indent = 4)
    fileW.close()
    print("The file has been written successfully!\n")

# Read from file

def json_reading(Dict: dict):
    fileR = open("Beer.json", "r", encoding = "utf-8")
    data_from_file = json.load(fileR)
    fileR.close()
    Dict.clear()
    Dict.update(data_from_file)
    
    print("The file has been read successfully!\n")

# Sort

def sort_dict():
    c = input("In which order do you want to sort the list?\n1.Ascending\n2.Descending\n")
    print("\n")
    if c == '1':
        for x, y in sorted(beer_dict.items()):
            print("Beer:", x, "\n% of alcohol:", y['alcho'], "\nIngredients:", y['ingredients'], "\nDescription:", y['description'], "\n")
    elif c == '2':
        for x, y in sorted(beer_dict.items(), reverse = True):
            print("Beer:", x, "\n% of alcohol:", y['alcho'], "\nIngredients:", y['ingredients'], "\nDescription:", y['description'], "\n")
    else:
        print("Wrong symbol!")

user_input = ""

while True:
    print("Choose your option:\n1. Show a list\n2. Add to the list\n3. Remove from the list\n4. Save to a file \
    \n5. Read from a file\n6. Sort the list\n7. Exit")
    user_input = input("Your choice: ")
    print("\n")
    match user_input:
        case "1":
            show_dict()
        case "2":
            add_dict()
        case "3":
            remove_dict()
        case "4":
            if len(beer_dict) != 0:
                json_writing(beer_dict)
            else:
                print("Your list is empty.\n")
        case "5":
            json_reading(beer_dict)
        case "6":
            sort_dict
        case "7":
            break
        case _:
            print("Wrong symbol!")


