IFS=""
num=1
outdir="img/"

while IFS="" read name; do
  outname="$outdir$num.gif"
  echo outname

  num=$(($num + 1)) # Increment num

  name=$(echo "$name" | tr '[:upper:]' '[:lower:]') # Convert name to lowercase

  echo "Current file: $outname"
  if [ -e $outname ] ; then # If the file exists then skip it
    echo "Image exists. Skipped $outname"
  else
    echo "Downloading $name.gif"
    curl http://www.pokestadium.com/img/sprites/main-series/xy/$name.gif -o $outname
  fi
done < text/names.txt

echo "Finished downloading images"
