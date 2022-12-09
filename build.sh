cd python
python CV_maker.py
python get_pub.py
python pub2tex.py
cd ../latex
rm build/*
latexmk
latexmk -c
cd ../
