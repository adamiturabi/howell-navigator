import sys
import csv

toc_csv_filename = sys.argv[1]
quarto_yaml_filename = '_quarto-basic.yml'

with open(quarto_yaml_filename, "a", encoding="utf-8") as file:
  file.write('book:\n')
  file.write('  chapters:\n')
  file.write('    - index.qmd\n')

with open(toc_csv_filename, newline='') as toc_csv:
  #csv_data = csv.reader(toc_csv, delimiter=',')
  fieldnames = ['part', 'chapter', 'title', 'section', 'toc_pagenum']
  csv_data = csv.DictReader(toc_csv, delimiter=',', fieldnames=fieldnames)

  curr_chapter = ''
  curr_part = ''

  for row in csv_data:
    print(row)
    new_part = False
    new_chapter = False

    if row['part'] != '':
      curr_part = row['part']
      new_part = True

    if row['chapter'] != '':
      curr_chapter = row['chapter']
      new_chapter = True

    chapter_filename = curr_part + '-' + curr_chapter.zfill(2) + '.qmd'
    print(chapter_filename)

    with open(quarto_yaml_filename, "a", encoding="utf-8") as file:
      if new_part:
        file.write('    - part: "Part ' + curr_part + '"\n')
        file.write('      chapters:\n')
      if new_chapter:
        file.write('        - "content/' + chapter_filename + '"\n')

    with open('content/' + chapter_filename, "a", encoding="utf-8") as file:
      file.write("#")
      if not new_chapter:
        file.write("#")
      file.write(" " + row['title'] + "\n\n") 
      file.write('<iframe src="combined-toc.pdf#page=' + row['toc_pagenum'] + '" width="100%" height="900px"></iframe>\n\n')


