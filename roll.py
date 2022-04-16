import quantumrandom
import re

# This one was quick and particularly spaghetti. Apologies to any viewers or my future self.
# TODO: case of single signed positive int, e.g. "+8"
# Potential todo: lone integer with comment, e.g. "8 initiative"

def roll(received):
    dice = []
    modifiers = []
    inputs = []
    rolls = []
    modtotal = 0
    total = 0
    comment = ""
    response = ""

    try:
        # Strip any text after last integer to allow for comments
        pos = re.match('.+([0-9])[^0-9]*$', received)
        pos = pos.start(1)
        comment = received[pos+1:len(received)] 
        received = received[0:pos+1]
    except:
        # No comment
        pass

    # Remove spaces
    received = ''.join(received.split())

    if len(received) == 0:
        # Nothing to roll, empty input
        return "```\n0 [Empty input]\n```"

    # Split our additions
    inputs = received.split("+")
    # Attempt to roll
    for item in inputs:
        if 'd' in item:
            # This is a die roll, split it up and roll them
            die = item.split("d")
            try:
                if len(die) > 2:
                    raise ValueError("A dice roll contained more than one dice definition: " + item)
                count = int(die[0])
                sides = int(die[1])
                for _ in range(count):
                    result = int(quantumrandom.randint(1, sides))
                    dice.append("1d" + str(sides))
                    rolls.append(result)
            except Exception as ex:
                # Negative numbers can end up here because I'm bad at structuring code
                sublist = item.split("-")
                if len(sublist) > 0:
                    # Negative number
                    modifiers.append(-abs(int(sublist[1])))
                    die = sublist[0].split("d")
                    if len(die) > 2:
                        return "Roll module failure"
                    count = int(die[0])
                    sides = int(die[1])
                    for _ in range(count):
                        result = int(quantumrandom.randint(1, sides))
                        dice.append("1d" + str(sides))
                        rolls.append(result)
                    pass
                else:
                    response = "Error: The Roll module failed to roll '" + item
                    response += "'. Please check your input and try again."
                    return response
        else:
            # This is a modifier, positive or negative
            try:
                modifier = int(item)
                modifiers.append(modifier)
            except:
                # This was a string buried inside our rolls, or a -int roll.
                foundint = 0
                negatives = []
                positives = []
                if '-' in item:
                    negatives = item.split("-")
                if len(negatives) > 0:
                    # Found a potential negative number
                    modifiers.append(int(negatives[0]))
                    modifiers.append(-abs(int(negatives[1])))
                    foundint = 1
                if foundint:
                    continue
                
                # If we make it here, invalid roll
                response = "Error: The Roll module saw '" + item
                response += "' as an invalid roll. Please check your input and try again."
                return response

    # We've succesfully rolled everything! Compile results.
    response = "```\n"
    if len(comment) > 1:
        response += "Rolling for" + comment + "...\n"
    else:
        response += "Rolling...\n"

    # Build up output for dice rolled
    if len(dice) > 0:
        response += str(dice[0])
        for itr in range(len(dice)):
            if itr != 0:
                response += " + " + str(dice[itr])
    # Build up output for modifiers entered
    if len(modifiers) > 0:
        response += " [+" + str(modifiers[0])
        for itr in range(len(modifiers)):
            if itr != 0:
                response += " + " + str(modifiers[itr])
            modtotal += modifiers[itr]
            total += modifiers[itr]
        response += "]"

    # Calculated/rolled outputs
    response += " =>"

    if len(rolls) > 0:
        response += " " + str(rolls[0])

        for itr in range(len(rolls)):
            if itr != 0:
                response += " + " + str(rolls[itr])
            total += rolls[itr]

    # Calculated modifier output
    if modtotal > 0:
        response += " [+" + str(modtotal) + "]"
    elif modtotal < 0:
        response += " [" + str(modtotal) + "]"

    # Final result
    response += "\n= " + str(total)
    response += "\n```"

    return response
