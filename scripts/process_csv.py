import sys
import csv
#,,Preface,,1,2
#,,Additions and corrections,,1,44
#,,Abbreviations of References,,1,45
#,,Chronological list of grammarians,,1,71
#,,Abbreviations of technical terms,,1,79
#,,Glossary of technical terms,,1,81
#,,Introduction,1,1

toc_csv_filename = sys.argv[1]
quarto_yaml_filename = '_quarto-basic.yml'
fastnav_csv_filename = sys.argv[2]
sec_pagenum_dict = {}
part_names = {"1": "The noun (§§ 2--401)", "2": "The  verb (§§ 402--496A)", "3": "The particle (§§ 497--624)", "4": "The common processes (§§ 625--759)" }

def get_section_url(key):
  values = sec_pagenum_dict[key]
  url = "https://archive.org/stream/howellarabicgrammar2013/howell-arabicgrammar-snap-book"
  url += values['book_num']

  book_pagenums_dict = {
    "1": "_1-498",
    "2": "_499-861",
    "3": "_862-1422",
    "4": "_1423-1813",
    "5": "_1-735",
    "6": "_736-1662",
    "7": "_1663-1850",
  }
  url += book_pagenums_dict[values['book_num']]
  url += '#page/n'
  pagenum = int(values['2013_pdf_pagenum'])
  pagenum -= 1
  url += str(pagenum)
  url += '/mode/1up'
  return url

with open(fastnav_csv_filename, newline='') as fastnav_csv:
  csv_data = csv.DictReader(fastnav_csv, delimiter=',')
  for row in csv_data:
    sec_num = row.pop('sec_num', None)
    assert(sec_num[0] == 'S')
    assert(sec_num[-1] == '.')
    sec_num = sec_num[1:-1]
    sec_pagenum_dict[sec_num] = row
  #print(sec_pagenum_dict)

with open(quarto_yaml_filename, "a", encoding="utf-8") as file:
  out_str = """
book:
  chapters:
    - index.qmd
    - part: "Frontmatter"
      chapters:
        - "content/preface.qmd"
        - "content/add_corr.qmd"
        - "content/abbrev_ref.qmd"
        - "content/grammarians.qmd"
        - "content/abbrev_tech.qmd"
        - "content/gloss_tech.qmd"
    - "content/intro.qmd"
"""
  file.write(out_str)

with open(toc_csv_filename, newline='') as toc_csv:
  #csv_data = csv.reader(toc_csv, delimiter=',')
  csv_data = csv.DictReader(toc_csv, delimiter=',')

  curr_chapter = ''
  curr_part = ''
  curr_subchapter = ''

  sec_pagenum_dict_keys = list(sec_pagenum_dict.keys())

  for row in csv_data:
    #print(row)
    new_part = False
    new_chapter = False

    if row['part'] != '':
      curr_part = row['part']
      new_part = True

    if row['chapter'] != '':
      curr_chapter = row['chapter']
      new_chapter = True
      curr_subchapter = 0
    else:
      curr_subchapter += 1

    chapter_filename = curr_part + '-' + curr_chapter.zfill(2) + '-' + str(curr_subchapter) + '.qmd'
    #print(chapter_filename)

    with open(quarto_yaml_filename, "a", encoding="utf-8") as file:
      if new_part:
        file.write('    - part: "Part ' + curr_part + ': ' + part_names[curr_part] + '"\n')
        file.write('      chapters:\n')
      #if new_chapter:
      file.write('        - "content/' + chapter_filename + '"\n')

    with open('content/' + chapter_filename, "a", encoding="utf-8") as file:
      file.write("#")
      #if not new_chapter:
      #  file.write("#")
      file.write(" ")
      if new_chapter:
        file.write(curr_chapter + ' ')
      else:
        file.write("---")

      section_beg = row['section_beg']
      section_end = row['section_end']
      title_section_str = '§\\ ' + section_beg
      if section_beg != section_end:
        title_section_str = '§' + title_section_str + '--' + section_end

      file.write(row['title'] + " (" + title_section_str + ") {.unnumbered}\n\n") 

      iframe_str = '```{=html}\n'
      iframe_str += '<iframe src="combined-toc.pdf#page=' + row['toc_pagenum'] + '" width="39%" height="900px"></iframe>\n'

      if section_beg == section_end:
        # automatically open section
        section_url = get_section_url(section_beg)
        iframe_str += '<iframe src="' + section_url + '" width="59%" height="900px" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe>\n'
      else:
        # present section list
        curr_key_idx = sec_pagenum_dict_keys.index(section_beg)
        end_key_idx = sec_pagenum_dict_keys.index(section_end)
        section_list_str = '<p><ul>'
        while True:
          curr_key = sec_pagenum_dict_keys[curr_key_idx]
          section_list_str += '<li><a href='
          section_list_str += get_section_url(curr_key)
          #section_list_str += 'https://archive.org/embed/howellarabicgrammar2013/howell-arabicgrammar-snap-book1_1-498#page/n132/mode/1up'
          section_list_str += '>§&nbsp' + curr_key + '</a></li>'
          if curr_key_idx == end_key_idx:
            break
          curr_key_idx += 1

        section_list_str += '</ul></p>'
        #file.write(section_list_str)

        iframe_str += '<iframe srcdoc="' + section_list_str + '" width="59%" height="900px" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe>\n'

      iframe_str += '```\n\n'
      file.write(iframe_str)

      #file.write('<iframe src="combined-toc.pdf#page=' + row['toc_pagenum'] + '&zoom=120" width="39%" height="900px"></iframe>\n\n')
      #file.write('<iframe src="combined-toc.pdf#page=' + row['toc_pagenum'] + '&zoom=page-width" width="59%" height="900px"></iframe>\n\n')


