echo "Are you sure you want to build the database? All existing data will be erased"
echo "yes or no (y/n):"
read choice

# db/ contains all logic and data to initialize the database
cd db

if [ $choice == 'y' ] ; then
  rm -f pokemon.db
  touch pokemon.db
  sqlite3 pokemon.db < buildDatabase.sql
  python buildDatabase.py
  echo "Finished building database"
else
  echo "Did not build database"
fi

echo ""
