import json
GAME = {
    '__metadata__': {
        'title': 'The Glass House',
        'start': 'Path_to_Glass_House'
    }
}
def create_room(name, description, ends_game=False, first_time=None):
    assert (name not in GAME)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'items': [],
    }
    # Is there a special message for the first visit?
    if first_time:
        exit['first_time'] = first_time
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description, required_key=None, hidden=False):
    # Make sure source is our room!
    if isinstance(source, str):
        source = GAME[source]
    # Make sure destination is a room-name!
    if isinstance(destination, dict):
        destination = destination['name']
    # Create the "exit":
    exit = {
        'destination': destination,
        'description': description
    }
    # Is it locked?
    if required_key:
        exit['required_key'] = required_key
    # Do we need to search for this?
    if hidden:
        exit['hidden'] = hidden
    source['exits'].append(exit)
    return exit

glass_House_key = "Glass House Key"

Path_to_Glass_House = create_room("Path_to_Glass_House", """You are on the path to the modernist marvel in New Canaan CT.
How did you get here?""")
create_exit(Path_to_Glass_House, "underground_tunnel", "There are stairs leading down.")
create_exit(Path_to_Glass_House, "guest_house", "There is a path ahead.")
create_exit(Path_to_Glass_House, "kitchen", "There is a door.")
create_exit(Path_to_Glass_House, "outside", "The Glass House Key", required_key=glass_House_key)

underground_tunnel = create_room("underground_tunnel", """You have found the underground tunnel leading to the Guest House.
It is darker down here.
You get the sense a secret is nearby, but you only see the tunnel from which you came from.""")
create_exit(underground_tunnel, Path_to_Glass_House, "There are stairs leading up.")
create_exit(underground_tunnel, "secretRoom", "A trapdoor was hidden amongst the dust.", hidden=True)

guest_house = create_room("Guest House", """The underground tunnel leads you to a beautiful, enclosed, yet peculiar bedroom. 
It's dim and cozy in here.""")
create_exit(guest_house, Path_to_Glass_House, "There is a path leading to the Glass House.")
create_exit(guest_house, "Pavillion", "There is a slide.")

pavillion = create_room("Pavillion", """There's definitely something large moving in the pond. 
This part of the estate is more open, so maybe you'd like it here.""")
create_exit(pavillion, guest_house, "There is a path leading to the Guest House.")
create_exit(pavillion, "balcony", "A small door rattles in the wind.")
create_exit(pavillion, "dumbwaiter", "There is a dumbwaiter near the chimney.")

painting_gallery = create_room("painting_gallery", """There's a strange painting here on that looks like a switch.""")
painting_gallery["items"].append(glass_House_key)
create_exit(painting_gallery, "simulation", "Fiddle with the switch.")
create_exit(painting_gallery, "pavillion", "Go back to the pavillion.")

create_room("simulation", """You were inside a virtual simulation exploring the Glass House.
...
I guess you escaped.""", ends_game=True)

kitchen = create_room("kitchen", """You've found the kitchen. Everything looks sleek and like I'm not supposed to touch it.""")
create_exit(kitchen, Path_to_Glass_House, "There is a door.")
create_exit(kitchen, "cylindrical_bathroom", "There is a peculiar bathroom.")

cylindrical_bathroom = create_room("cylindrical_bathroom", """You explore the cylindrical bathroom. What are you doing?""")
create_exit(cylindrical_bathroom, pavillion, "Exit down the hill.")
create_exit(cylindrical_bathroom, kitchen, "Exit on the right.")
create_exit(cylindrical_bathroom, "secretRoom", "Exit at the bottom.")

dumbwaiter = create_room("dumbwaiter", """You crawl into the dumbwaiter. What are you doing?""")
create_exit(dumbwaiter, kitchen, "Exit on the first-floor.")
create_exit(dumbwaiter, "secretRoom", "Exit at the bottom.")

secretRoom = create_room("secretRoom", """You have found the secret room.
Who thought more Barcelona chairs a good idea?""")
create_exit(secretRoom, "hallway0", "A long hallway leads away.")
create_exit(secretRoom, underground_tunnel, "You see a trapdoor with a spider crawling on it.")
create_exit(secretRoom,cylindrical_bathroom, "Get back in the dumbwaiter.")

crypt = create_room("crypt", """You've found your way into a crypt. You smell dirt.""")
create_exit(crypt, "outside", "There are stairs leading up.")
outside = create_room("outside", """You step out into the night.

It smells like freedom.
""", ends_game=True)

hallway_length = 3
for i in range(hallway_length):
    here = "hallway{}".format(i)
    forward = "hallway{}".format(i+1)
    backward = "hallway{}".format(i-1)
    if i == 0:
        backward = "secretRoom"
    elif i == hallway_length - 1:
        forward = "crypt"
    create_room(here, """This is a very long hallway.""")
    create_exit(here, backward, """Go back.""")
    create_exit(here, forward, """Go forward.""")
    #add the new function statement here 

##
# Save our text-adventure to a file:
##
with open('theGlassHouse.json', 'w') as out:
    json.dump(GAME, out, indent=2)