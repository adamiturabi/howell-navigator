#!/usr/local/bin/bash
rm -rf content/*
cp srcqmd/*.qmd content
quarto render --profile makehtml

