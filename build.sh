cd python
python get_pub.py
python pub2tex.py
python CV_maker.py
cd ../latex
latexmk
latexmk -c
cd ../
