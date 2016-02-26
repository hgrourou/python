echo "arg1 = $1;"
cat ../download/gengxin.txt  |while  read LINE
do
	wget --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -P $1  $LINE
done

zip ../PDF.zip ../pdf/*.pdf
./a.out ../

