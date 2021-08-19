def pkmn(received):
    # check for non-name argument
    try:
        argument, name = received.split(" ", 1)
    except:
        argument = ""
        append = ""
        name = received
        pass

    response = ""
    name = name.lower()
    argument = argument.lower()

    # Helper function for input checking
    def input_check(name, argument):
        if argument == "stats" or argument == "stat":
            return "#Stats"
        elif argument == "learnset" or argument == "moves" or argument == "learnlist":
            return "#Learnset"
        elif argument == "boop":
            if name.lower() == "espeon":
                return 100
            else:
                if "espeon" in name.lower():
                    return 101
                return 99
        else:
            return ""

    # If we got more than one input, try to match to a function
    if argument:
        append = input_check(name, argument)
        # Check if we got a result. If not, try swapping the arguments
        if not append:
            print("hit not append")
            name, argument = argument, name
            append = input_check(name, argument)
            # Check if we got a result. If not, give up and put the variables back to normal.
            if not append:
                print ("hit not not append")
                name, argument = argument, name

    if append == 99:
        response = ":point_right: "
        append = ""
    elif append == 100:
        return "Unfortunately, I am obligated to refuse this command by my creator."
    elif append == 101:
        return "Unfortunately, crafty though you may be, I am still obligated to refuse this command."

    response += "https://bulbapedia.bulbagarden.net/wiki/" + name + "_(Pok%C3%A9mon)" + append

    return response

