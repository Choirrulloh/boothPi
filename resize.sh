#!/bin/bash

# TODO: Take directory from $1 or something

tempdir="."

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

border_width=$[original_h * 5 / 100]
echo "    Border width is ${border_width}."

name_offset=$[ ${#tempdir} + 1 + 26 ]
echo "Filename offset is ${name_offset}."

echo "Creating target folders..."
mkdir -p merged/square
mkdir -p merged/line
mkdir -p merged/3lines
mkdir -p merged/webservice

echo "Creating square images..."
size=$square_size
offs=$square_offset
bord=$border_width
for i in ${sources[@]}; do
	base=${i:0:$name_offset}
	cmd="convert -size $[size*2 + bord*3]x$[size*2 + bord*3] xc:white "
	[ -f "${base}---1.jpg" ] && cmd="$cmd ${base}---1.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord] -composite "
	[ -f "${base}---2.jpg" ] && cmd="$cmd ${base}---2.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord*2+size]+$[bord] -composite "
	[ -f "${base}---3.jpg" ] && cmd="$cmd ${base}---3.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*2+size] -composite "
	[ -f "${base}---4.jpg" ] && cmd="$cmd ${base}---4.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord*2+size]+$[bord*2+size] -composite "
	cmd="$cmd merged/square/$(basename "${base}").jpg"
	$cmd
	echo -n "."
done
echo " done."

echo "Creating line images..."
for i in ${sources[@]}; do
	base=${i:0:$name_offset}
	cmd="convert -size $[size + bord*2]x$[size*4 + bord*5] xc:white "
	[ -f "${base}---1.jpg" ] && cmd="$cmd ${base}---1.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*1+size*0] -composite "
	[ -f "${base}---2.jpg" ] && cmd="$cmd ${base}---2.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*2+size*1] -composite "
	[ -f "${base}---3.jpg" ] && cmd="$cmd ${base}---3.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*3+size*2] -composite "
	[ -f "${base}---4.jpg" ] && cmd="$cmd ${base}---4.jpg[${size}x${size}+${offs}+0] -geometry ${size}x${size}+$[bord]+$[bord*4+size*3] -composite "
	cmd="$cmd merged/line/$(basename "${base}").jpg"
	$cmd
	echo -n "."
done
echo " done."

echo "Creating 3x line images..."
files=(merged/line/*.jpg)
size_w=$[size + bord*2]
size_h=$[size*4 + bord*5]
i=0
while [[ $i -lt ${#files[@]} ]] ; do
	file=${files[$i]}
	cmd="convert -size $[size_w*3]x${size_h} xc:white "
	[ -f "${files[$i]}" ] && cmd="$cmd ${files[$i]}   -geometry ${size_w}x${size_h}+$[size_w*0]+0 -composite "
	[ -f "${files[$i+1]}" ] && cmd="$cmd ${files[$i+1]} -geometry ${size_w}x${size_h}+$[size_w*1]+0 -composite "
	[ -f "${files[$i+2]}" ] && cmd="$cmd ${files[$i+2]} -geometry ${size_w}x${size_h}+$[size_w*2]+0 -composite "
	cmd="$cmd merged/3lines/$(basename "${file}")"
	$cmd
	echo -n "."
	i=$( expr $i + 3 )
done
echo " done."

echo "Creating photobox webservice images..."
for i in merged/square/*.jpg; do
	convert "$i" -resize 50% -quality 90 merged/webservice/$(basename "$i")
	echo -n "."
done
echo " done."
