#!/bin/bash
# mc_serv.sh -- interface with local minecraft servers to start and stop them on demand
# Parse inputs. Need a command and a server
while [[ $# -gt 0 ]]; do
  param="$1"

  case $param in
    -s|-S|--server|--Server)
      SERV="$2"
      shift # param
      shift # val
      ;;
    -c|-C|--command|--Command)
      CMD="$2"
      shift # param
      shift # val
      ;;
    *)
      echo "Invalid argument passed to mc_serv.sh."
      echo "Please use only -s/--server, -c/--command"
      exit 1
      ;;
  esac
done

function playerlist {
    # Populate list of players in screen
    screen -S $SERV -X stuff "`echo -ne \"list\r\"`"
    RC=$?
    if [ $RC -ne 0 ]; then
        echo "Failed to retrieve player list! RC: $RC"
	exit $RC
    fi
    # wait two seconds for list command
    sleep 1
    # Dump output to file
    screen -S $SERV -X hardcopy "playerlist.tmp"
    # Strip all text from output other than player count and players
    listplayers=$(cat playerlist.tmp | tail -n 3 | sed 's/^.*]:\s//g' | sed '$d')
    # Remove temp file
    rm -f playerlist.tmp > /dev/null
    return 0
}

if [ $CMD == "start" ]; then
    # Check if server exists
    if [ ! -f ~/mc_serv/$SERV/start-server.sh ]; then
        echo "Starting server returned an error! Server start script does not exist."
	exit 2
    fi
    # Start specified server
    screen -dmS $SERV
    screen -S $SERV -p 0 -X stuff "pushd ~/mc_serv/$SERV; ./start-server.sh\n"
    RC=$?
    if [ $RC -ne 0 ]; then
        echo "Starting server returned an error! RC: $RC"
	exit $RC
    fi
    echo "Server start script running!"
    exit 0
fi

if [ $CMD == "stop" ]; then
    # Stop server
    screen -S $SERV -X stuff "`echo -ne \"stop\r\"`"
    RC=$?
    if [ $RC -ne 0 ]; then
        echo "Stopping server returned an error! RC: $RC"
	exit $RC
    fi
    # wait 10 seconds, ctrl-c, quit session
    sleep 10
    screen -S $SERV -X stuff $'\003'
    screen -S $SERV -X quit
    echo "Server quit!"
    exit 0
fi

if [ $CMD == "save" ]; then
    # Save server
    screen -S $SERV -X stuff "`echo -ne \"save-all\r\"`"
    RC=$?
    if [ $RC -ne 0 ]; then
        echo "Saving world returned an error! RC: $RC"
	exit $RC
    fi
    exit 0
fi

if [ $CMD == "info" ]; then
    # return server info
    cat ~/mc_serv/$SERV/server-info.txt
    RC=$?
    if [ $RC -ne 0 ]; then
	if [ $RC == 1 ]; then
            echo "Failed to retrieve server info, the server $SERV does not exist!"
	else
            echo "Failed to retrieve server info!"
	fi

	exit $RC
    fi
    exit 0
fi

if [ $CMD == "list" ]; then
    # return list of servers
    pushd ~/mc_serv/ > /dev/null
    ls -1 -d */ | cut -f1 -d'/'
    popd > /dev/null
    exit 0
fi

if [ $CMD == "time" ]; then
    # return average start time of servers
    cat ~/mc_serv/$SERV/start-time.txt
    RC=$?
    if [ $RC -ne 0 ]; then
        echo "Failed to retrieve server info!"
	exit $RC
    fi
    exit 0
fi

if [ $CMD == "players" ]; then
    # Return current players
    playerlist
    echo $listplayers
    exit 0
fi
    
if [ $CMD == "op" ]; then
    # op all connected players
    playerlist
    # remove player count output, remove commas to make an array
    player_string=$(echo "$listplayers" | sed '1d' | sed 's/,\s/|/')
    if [ -z "$player_string" -a "$player_String" == " " ]; then
        echo "There are no players currently on the server to op!"
    else
	IFS='|' read -ra player_array <<< "$player_string"
        for player in "${player_array[@]}"; do
            screen -S $SERV -X stuff "`echo -ne \"op $player\r\"`"
            RC=$?
            if [ $RC -ne 0 ]; then
                echo "Failed to op player $player! RC: $RC"
	        exit $RC
            fi
	    echo "$player has been opped!"
        done
    fi
    exit 0
fi

echo "Unrecognized command passed to mc_serv.sh."
echo "Supported commands are info, save, start, or stop."
exit 1
