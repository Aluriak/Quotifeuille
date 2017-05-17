
FNAME=tables
PYTHON=python3
PDF_VIEWER=evince
LATEX_COMPILER=pdflatex


all: gen compile show

cs: compile show

gen:
	$(PYTHON) quotifeuille.py -o $(FNAME).tex
compile:
	$(LATEX_COMPILER) $(FNAME).tex
show:
	$(PDF_VIEWER) $(FNAME).pdf


_gen_empty:
	python quotifeuille.py --columns "" "\quad\quad\quad\quad\quad\quad\quad" "" "" "" -l 55
gen_empty: _gen_empty cs
_gen_my:
	python quotifeuille.py --columns biblio "lecture ($neg$ thèse)" "couché-tôt" sport code -l 55
gen_my: _gen_my cs
