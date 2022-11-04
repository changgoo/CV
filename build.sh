cd python
python get_pub.py
python pub2tex.py
cd ../latex
latexmk
latexmk -c
cd ../
