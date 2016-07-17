#!/usr/bin/bash

# TODO: Take directory from $1 or something

echo "Setting up Tempdir..."
tempdir=$(mktemp -d temp.XXXXXX)
trap 'echo "Removing Tempdir..."; rm -rf "$tempdir"; exit' EXIT INT TERM HUP

echo "    Tempdir is $tempdir"

echo "Copying files to tempdir..."
files=(*---?.jpg)

echo -n "    "
for i in ${files[@]}; do
	cp "$i" "$tempdir/$i"
	echo -n "."
done
echo " done."

#echo "Resizing images to 50%..."
#files=(*---?.jpg)
#
#echo -n "    "
#for i in ${files[@]}; do
#	convert "$i" -resize 50% "$tempdir/$i"
#	echo -n "."
#done
#echo " done."

echo "Reading image size..."
sources=($tempdir/*---1.jpg)
echo "    Using ${sources[0]}"
original_h=$(convert "${sources[0]}" -format "%h" -identify null:)
original_w=$(convert "${sources[0]}" -format "%w" -identify null:)
echo "    Image size is ${original_w}x${original_h}."

echo "Calculating target sizes..."
square_size=$[original_h]
echo "    Square size is ${square_size}x${square_size}."
square_offset=$[(original_w - original_h) / 2]
echo "    Square offset is ${square_offset}."

line_h=$original_h
line_w=$[original_h / 45 * 35]
echo "    Line size is ${line_w}x${line_h}."
line_offset=$[(original_w - line_w) / 2]
echo "    Line offset is ${line_offset}."

border_width=$[original_h * 5 / 100]
echo "    Border width is ${border_width}."

echo "Creating target folders..."
mkdir -p merged/square
mkdir -p merged/line
mkdir -p merged/3lines

echo "Creating square images..."
size=$square_size
offs=$square_offset
bord=$border_width
for i in ${sources[@]}; do
	base=${i:0:27}
	convert -size $[size*2 + bord*3]x$[size*2 + bord*3] xc:white \
		${base}---1.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord] -composite \
		${base}---2.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord*2+size]+$[bord] -composite \
		${base}---3.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*2+size] -composite \
		${base}---4.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord*2+size]+$[bord*2+size] -composite \
		merged/square/$(basename "${base}").jpg
	echo -n "."
done
echo " done."

echo "Creating line images..."
size_w=$line_w
size_h=$line_h
offs=$square_offset
bord=$border_width
for i in ${sources[@]}; do
	base=${i:0:27}
	convert -size $[size + bord*2]x$[size*4 + bord*5] xc:white \
		${base}---1.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*1+size*0] -composite \
		${base}---2.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*2+size*1] -composite \
		${base}---3.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*3+size*2] -composite \
		${base}---4.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*4+size*3] -composite \
		merged/line/$(basename "${base}").jpg
	echo -n "."
done
echo " done."

echo "Creating 3x line images..."
files=(merged/line/*.jpg)
bord=$border_width
size=$square_size
size_w=$[size + bord*2]
size_h=$[size*4 + bord*5]
i=0
while [[ $i -lt ${#files[@]} ]] ; do
	file=${files[$i]}
	convert -size $[size_w*3]x${size_h} xc:white \
		${files[$i]}   -geometry ${size_w}x${size_h}+$[size_w*0]+0 -composite \
		${files[$i+1]} -geometry ${size_w}x${size_h}+$[size_w*1]+0 -composite \
		${files[$i+2]} -geometry ${size_w}x${size_h}+$[size_w*2]+0 -composite \
		merged/3lines/$(basename "${file}")
	echo -n "."
	i=$( expr $i + 3 )
done
echo " done."