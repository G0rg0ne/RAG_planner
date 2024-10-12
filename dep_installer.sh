while read line; do
    poetry add "$line"
done < requirements.txt