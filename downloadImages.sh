# The URLs used in this file are no longer valid, therefore this script is broken
# Feel free to use or modify in any way

# IFS="" # Input file stream
# num=1 # Counter/Dational Dex number
# outdir="img/"
#
# while IFS="" read name; do
#   outname="$outdir$num.gif"
#   echo outname
#
#   num=$(($num + 1)) # Increment num
#
#   name=$(echo "$name" | tr '[:upper:]' '[:lower:]') # Convert name to lowercase
#
#   echo "Current file: $outname"
#   if [ -e $outname ] ; then # If the file exists then skip it
#     echo "Image exists. Skipped $outname"
#   else
#     echo "Downloading $name.gif"
#     curl http://www.pokestadium.com/img/sprites/main-series/xy/$name.gif -o $outname
#   fi
# done < text/names.txt
#
# echo "Finished downloading images"
