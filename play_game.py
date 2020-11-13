import json
import os
import time
import random 

def main():
    # TODO: allow them to choose from multiple JSON files?
    for file in os.listdir():
        if file.endswith(".json"):
            print (file)
    json_file = input("Which file will you open? ") 
    
    with open("theGlassHouse1.json") as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)
    

def play(rooms):
    current_time= time.time()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    visited = {}

    while True:
        # Figure out what room we're in -- current_place is a name.
        times= int(time.time() - current_time)
       
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        print ("You have been here for " + str(times) +" seconds")
        
        if here ["items"] == []:
            print ("There is nothing here for you to take.")
        else:
            print ("You can take" + str(here["items"]))
        
        cat_s = "not seen" 
        cat = random.randint(0, 7)
        if cat_s == "seen":
            if cat == 1:
                print ("You spot the cat again! So pretty!")
                
            if cat == 2:
                print ("You see some lonely fur.")
        else:
            if cat == 1:
                print ("You spot a black cat!")
                cat_s = "seen"
            
        if here.get("visited", False):
            print ("You've been in this room before.")
        here ['visited'] = True 

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
#         unlocked_exits = usable_exits[0]
#         locked_exits = usable_exits [1]

        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()
        
        if action == "help":
            print_instructions ()
            continue 
        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit. Better luck next time!")
            break

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if stuff == []:
                     print ("You have nothing.")
            else:
                print(stuff)

            continue
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            if here ["items"] == []:
                     print ("There is nothing here for you to take.")
            else:
                print ("You picked up", + here ["items"])
                stuff.extend(here["items"])
                here["items"].clear()
            continue
        #TODO: If they type "drop", drop specific item and attach it to current location
        if action == "drop":
            drop = -1 
            while drop != 0: 
                print ("Which item do you want to drop?")
                for i, item in enumerate (stuff):
                    print ("   {}. {}".format (i+1, item))
                    
                drop= input(">").lower().strip()
                if int (drop) > len(stuff) or int(drop) < 0: 
                    print ("That's not an item.")
                else:
                    drop = int(drop)
                    here ["items"].append(stuff [drop -1])
                    stuff.pop(drop - 1)
                    drop = 0 
                
            continue
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    locked = []
    unlocked = [] 
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue 
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
