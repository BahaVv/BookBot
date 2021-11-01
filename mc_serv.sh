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

echo "Unrecognized command passed to mc_serv.sh."
echo "Supported commands are info, save, start, or stop."
exit 1
