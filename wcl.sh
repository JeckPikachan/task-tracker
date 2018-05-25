lines=0
for file in $(find . -name "*.py"); do
 lines=$(( $lines + $(cat $file | wc -l) ));
done;
echo $lines
