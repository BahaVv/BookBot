import os
import subprocess
import sys
import time

def help(serv):
    response = "```\n"
    response += "Available Commands for mc Module:\n\n"
    response += "!mc help: Shows this help text.\n"
    response += "!mc info: Get info for current server. Can also specify server to get info for.\n"
    response += "!mc list: List all available servers.\n"
    response += "!mc restart: Restart server, if running.\n"
    response += "!mc save: Save progress in current server. Done automatically when stopping server.\n"
    response += "!mc start -server-: Start selected server, shutting down current server if necessary.\n"
    response += "!mc stop: Stop current server. Takes 10 seconds.\n"
    response += "```"
    return response

# Helper function to get server from text file
def get_serv():
    serv_file = open("mc_serv.txt", "r+")
    serv = serv_file.readline().strip()
    serv_file.truncate()
    serv_file.close()
    return serv.strip()

# Helper function to set server in text file
def set_serv(serv):
    serv_file = open("mc_serv.txt", "w")
    serv_file.write(serv.strip())
    serv_file.close()
    return 0

# Helper function to get the timestamp of the start time of the current server
def get_timestamp():
    time_file = open("mc_time.txt", "r+")
    time = int(time_file.readline().strip())
    time_file.truncate()
    time_file.close()
    return time

# Helper function to set the timestamp of the start time of the current server
def set_timestamp():
    time_file = open("mc_time.txt", "w")
    current_time = int(time.time())
    time_file.write(str(current_time))
    time_file.close()
    return 0

# Helper function to get the average start time of a server 
def get_avg_start(serv):
    result = subprocess.run(['./mc_serv.sh', '-s', serv, '-c', 'time'], stdout=subprocess.PIPE)
    response = result.stdout.decode('utf-8').strip()
    return int(response)

# Helper function to generate responses
def return_check(RC, cmd):
    success = {
        'save': 'The server `XYZZY` has been manually saved!',
        'start': 'The server `XYZZY` is currently starting. It should take roughly YZZYX seconds to come online.',
        'stop': 'Terribly sorry for the delay, but the requested server, `XYZZY`, has now been stopped.'
    }

    failure = {
        'save': 'An error occurred while trying to save server `XYZZY`.\n',
        'start': 'An error occurred while trying to start server `XYZZY`.\n',
        'stop': 'An error occurred while trying to stop server `XYZZY`.\n'
    }
    if RC != 0:
        response = failure[cmd]
        response += "Please contact your server administrator for more info."
    else:
        response = success[cmd]
    return response

# Get info of current or arbitrary server.
def info(serv):
    current_serv = get_serv()

    if serv == "" and current_serv ==  "":
        response = "There doesn't appear to be a server running presently. "
        response += "If you wanted information for a specific server, try specifying with `!mc info -server-`."
        return response
    
    response = "```\n"
    
    if current_serv != "":
        response += "The server " + current_serv + " is currently running.\n\n"

    if serv == "":
        serv = current_serv

    response += "Description for " + serv + ":\n"

    result = subprocess.run(['./mc_serv.sh', '-s', serv, '-c', 'info'], stdout=subprocess.PIPE)
    response += result.stdout.decode('utf-8')
    response += "```"
    return response

def list(serv):
    result = subprocess.run(['./mc_serv.sh', '-s', serv, '-c', 'list'], stdout=subprocess.PIPE)
    response = "```\n"
    response += "Current List of Available Servers:\n\n"
    response += result.stdout.decode('utf-8')
    response += "```"
    return response

# Restart the server, if running.
def restart(serv):
    if serv == "":
        serv = get_serv()
        if serv == "":
            return "My apologies, but no server is currently running to restart!"
    return start(serv)

# Save manually
def save(serv):
    if serv == "":
        serv = get_serv()
    RC = subprocess.call(['./mc_serv.sh', '-s', serv, '-c', 'save'])
    return return_check(RC, 'save').replace("XYZZY", serv)

# Start the specified server, if it exists.
def start(serv):
    if serv == "":
        response = "I'm sorry, but you'll have to provide me with the name of a server to start." 
        response += "Try `!mc help` for more information."
        return response
    check_serv = get_serv()
    if check_serv != "":
        stop_str = stop(check_serv)
        if "error" in stop_str:
            if "seconds" in stop_str:
                response = stop_str
            elif serv == check_serv:
                response = "I'm sorry, but an error occurred while restarting server " + serv + ".\n"
                response += "Please reach out to the administrator for more info."
            else:    
                response = "An error occurred while trying to stop server " + check_serv + "to start server " + serv + ".\n"
                response += "Please contact your server administrator for more info."
            return response
    RC = subprocess.call(['./mc_serv.sh', '-s', serv, '-c', 'start'])
    if RC == 0:
        # Starting! So set the server and timestamp.
        set_serv(serv)
        set_timestamp() 

    avg_time = str(get_avg_start(serv))
    return return_check(RC, 'start').replace("XYZZY", serv).replace("YZZYX", avg_time)

# Stop the server given, or specified in the text file.
def stop(serv):
    if serv == "":
        # Assume user just wants to stop the running server and check again
        serv = get_serv()
        if serv == "":
            return "A running server could not be found, and no server was specified. There is nothing to stop."

    # Make sure enough time has passed to stop server
    time_since_start = int(time.time()) - get_timestamp()
    avg_time = get_avg_start(serv)

    if avg_time > time_since_start:
        response = "My humblest apologies, but there's been an error. `"
        response += serv + "` cannot be safely stopped or restarted until it has fully come online. "
        response += "Please try that again in another " + str(time_since_start - avg_time) + " seconds."
        return response

    RC = subprocess.call(['./mc_serv.sh', '-s', serv, '-c', 'stop']) 
    if RC == 0:
        set_serv("")
    response = return_check(RC, 'stop').replace("XYZZY", serv) 
    return response

def mc(received):
    # check for argument and sub-command
    try:
        command, serv = received.split(" ", 1)
    except:
        # Just an argument, no server
        command = received
        serv = ""
        pass

    response = ""
    command = command.lower()
    serv = serv.lower()

    commands = {
        '': help,
        'help': help,
        'info': info,
        'list': list,
        'restart': restart,
        'save': save,
        'start': start,
        'stop': stop
    }

    try:
        # Check if argument matches known command
        response = commands[command](serv)
    except Exception as ex:
        print(ex)
        # No command match
        response = "The minecraft module didn't recognize your input as a valid command. Try !mc help for more info."

    return response
