#!/usr/bin/env bash

wdir="$(dirname $0)"
deploydir="/var/www/html/can"
url="localhost/can"
src="src"
browser="chromium-browser"
# browser=firefox
databaseDir="db"
databaseName="can.sqlite"
initsql="initdb.sql"
databaseFile="$deploydir/$databaseDir/$databaseName"

echo "change working dir: '$wdir'"
cd "$wdir"

if [[ $1 == 'clean' ]]; then
	echo "remove old deployment '$deploydir'"
	sudo rm -rf "$deploydir"
fi

echo "copy src to '$deploydir'"
# sudo mkdir "$deploydir"
sudo rsync -a "$src/"* "$deploydir"

if [[ -f "$databaseFile" ]]; then
	echo "I found '$databaseFile' and I will use it."
else
	echo "I cannot find database. I will create a new one."
	sudo mkdir -p $deploydir/$databaseDir
	sudo chmod 777 $deploydir/$databaseDir
	cat "$initsql" | sudo sqlite3 "$databaseFile"
	sudo chmod 666 "$databaseFile"
fi

# always restart
# if [[ $1 == "restart" || $1 == "clean" ]]; then
echo "restart apache2"
sudo service apache2 restart
# fi

echo "open url '$url'"
"$browser" "$url"

