
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
