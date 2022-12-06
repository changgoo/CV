cd python
python CV_maker.py
python get_pub.py
python pub2tex.py
cd ../latex
latexmk
latexmk -c
cd ../
