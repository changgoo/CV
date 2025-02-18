$pdf_mode = 1;        # tex -> pdf
$latex = 'latex -interaction=nonstopmode -shell-escape';
$pdflatex="pdflatex -interaction=nonstopmode %O %S";
$out_dir = 'build';
@default_files = ('CV.tex', 'pub.tex', 'CV_pub.tex', 'ref.tex', 'key_pub.tex', 'CV_2025_review.tex');
