$pdf_mode = 1;        # tex -> pdf
$latex = 'latex -interaction=nonstopmode -shell-escape';
$pdflatex="pdflatex -interaction=nonstopmode %O %S";
$out_dir = 'build';
@default_files = ('CV_C7.tex');
