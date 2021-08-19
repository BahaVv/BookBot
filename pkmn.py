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
                return 99
        else:
            return ""

    # If we got more than one input, try to match to a function
    if argument:
        append = input_check(name, argument)
        # Check if we got a result. If not, try swapping the arguments
        if not append:
            name, argument = argument, name
            append = input_check(name, argument)
            # Check if we got a result. If not, give up and put the variables back to normal.
            if not append:
                name, argument = argument, name

    if append == 99:
        response = ":point_right: "
        append = ""

    response += "https://bulbapedia.bulbagarden.net/wiki/" + name + "_(Pok%C3%A9mon)" + append

    return response

