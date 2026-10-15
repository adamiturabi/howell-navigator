#!/usr/local/bin/bash
rm -f _quarto-basic.yml
rm -rf content/*
python3 scripts/process_csv.py scripts/toc.csv scripts/fastnav.csv
#cp srcqmd/*.qmd content
quarto render --profile makehtml
cp srcpdf/combined-toc.pdf docs/content/

