import re,os
import json
import glob

files = glob.glob('../data/*.json')
items = [os.path.basename(f).replace('.json','') for f in files]
div_line = r"%"+80*'='
publist = ['1st','2nd','co','review','prep','proc']
def add_header(fp):
  header = []
  # header.append(r"\documentclass[12pt,preprint,letter]{aastex63}")
  header.append(r"\documentclass[12pt]{article}")
  header.append(r"\usepackage{mycvstyle}")
  header.append(r"\pagestyle{CV}")

  for t in header:
    fp.write(t)
    fp.write('\n')

def add_affiliation(fp):
  texts = []
  texts.append(r"\begin{center}")
  texts.append(r"{\large \bf Curriculum Vitae -- Chang-Goo Kim}")
  texts.append(r"\end{center}")
  texts.append(div_line)

  texts.append(r"Department of Astrophysical Sciences")
  texts.append(r"\hfill +1-609-933-1180\\")
  texts.append(r"Princeton University")
  texts.append(r"\hfill \url{http://changgoo.github.io}\\")
  texts.append(r"4 Ivy Lane, Princeton")
  texts.append(r"\hfill \href{http://orcid.org/0000-0003-2896-3725}"
               r"{ORCID: 0000-0003-2896-3725}\\")
  texts.append(r"NJ 08544, USA")
  texts.append(r"\hfill \url{cgkim@astro.princeton.edu}")
  for t in texts:
    fp.write(t)
    fp.write('\n')

def get_text(item, data):
  istalk = False
  isref = True if item == 'references' else False
  iselem = False
  if item in ['invited_review_talks','invited_colloquia',
              'conference_workshop_seminar_talks',
              'professional_presentations'
              ]:
    istalk = True
  if item in ['education',
              'current_position',
              'employment',
              'research_advising',
              'teaching'
              ]:
    iselem = True
  if isref:
    text_format = [r"{{\small {{\bf Prof. {d[name]}}}",
            r"\url{{{d[email]}}}\\",
            # r"{d[phone]}\\",
            # r"{d[title]}, ",
            r"{d[affil]}}}",
            '\n'
            ]
  else:
    if iselem:
      head = '\n'+r"\elements{{"
    else:
      head = r"\onelineelements{{"

    if data['y2'] == 'None':
      year = r"{d[y1]}"
    else:
      if data['y1'].startswith('2'):
        year = r"{d[y1]} -- {d[y2]}"
      else:
        year = r"{d[y1]} -- \\ {d[y2]}"
    if istalk:
      text_format = [head + year +r"}}",
              r"{{{d[talk]}}}",
              r"{{\emph{{{d[title]}}},",
              r"{d[conf]},",
              r"{d[venue]}}}",
              ]
    else:
      text_format = [head + year +r"}}",
              r"{{{d[title]}}}",
              r"{{{d[other]}}}",
              ]
  try:
    text = '\n'.join(text_format).format(d=data)
    if istalk: text += '\n'
    return text
  except KeyError:
    print(item,data)
    return

def add_item(item,fp):
  data = json.load(open(os.path.join('../data',item+'.json')))

  fp.write(div_line)
  fp.write('\n\n')
  fp.write(r"\itemtitle{{{}}}".format(item.replace('_',' ').capitalize()))
  fp.write('\n\n')
  for d in data:
    if item == 'references':
      if d['type'] != 'main': continue
    text = get_text(item, d)
    fp.write(text)
    fp.write('\n')

def add_pubheader(fp,header=False, talk=False):
  texts = []
  if header:
    # header.append(r"\documentclass[12pt,preprint,letter]{aastex63}")
    texts.append(r"\documentclass[12pt]{article}")
    texts.append(r"\usepackage{mycvstyle}")
    texts.append(r"\pagestyle{pub}")
  else:
    texts.append(r"\begin{center}")
    if talk:
      texts.append(r"{\large \bf List of Professional Presentations}")
    else:
      texts.append(r"{\large \bf List of Publications}")
      texts.append(r"(\href{\adsurl}{ADS}, \href{\googleurl}{Google Scholar})\\")
      # texts.append(r"\\{\student{Name}: student advised/co-advised by me}\\")
      texts.append(r"\input{../data/summary.tex}")
    texts.append(r"\end{center}")
    texts.append(div_line)

  for t in texts:
    fp.write(t)
    fp.write('\n')

def add_pubitem(item,fp):
  fname = os.path.join('../data','pubs_ref_{}.tex'.format(item))
  summary_fname = os.path.join('../data','summary_{}.tex'.format(item))

  fp.write(div_line)
  fp.write('\n\n')
  if item == 'proc':
    fp.write(r"\itemtitle{Conferecne Proceedings/White Papers}")
  elif item in ['arXiv','prep']:
    fp.write(r"\itemtitle{Papers in Preparation}")
    fname = os.path.join('../data','pubs_{}.tex'.format(item))
  elif item in ['review']:
    fp.write(r"\itemtitle{Papers under Review}")
    fname = os.path.join('../data','pubs_{}.tex'.format(item))
  else:
    fp.write(r"\itemtitle{{Refereed Publications \input{{{}}}}}".format(summary_fname))
  fp.write('\n\n')
  if item == '2nd':
    fp.write(r"{\student{Name}: student advised/co-advised by me}")
  fp.write('\n')
  fp.write(r"\begin{itemize}[itemsep=0pt,topsep=\parskip]")
  fp.write('\n')
  fp.write(r"\small \input{{{}}}".format(fname))
  fp.write('\n')
  fp.write(r"\end{itemize}")
  fp.write('\n\n')
  fp.write(div_line)
  fp.write('\n\n')

def create_pub():
  fp = open('../latex/pub.tex','w')
  add_pubheader(fp,header=True)
  fp.write(r"\begin{document}"+'\n')

  add_pubheader(fp)
  for item in publist:
    add_pubitem(item,fp)

  add_pubheader(fp,talk=True)
  # for item in ['invited_review_talks',
  #               'invited_colloquia',
  #               'conference_workshop_seminar_talks']:
  for item in ['professional_presentations']:
    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write(r"\end{document}"+'\n')
  fp.close()

def create_CV():
  itemlist=['education',
            'current_position',
            'employment',
            'grants',
            'research_advising',
            'teaching',
            'computing_time_allocations',
            'observing_proposals',
            'scientific_collaboration_teams',
            'professional_service',
            'references'
            ]
  fp = open('../latex/CV.tex','w')
  add_header(fp)
  fp.write(r"\begin{document}"+'\n')

  add_affiliation(fp)
  for item in itemlist:

    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write(r"\end{document}"+'\n')
  fp.close()

def create_CV_pub():
  itemlist=['education',
            'current_position',
            'employment',
            'grants',
            'research_advising',
            'teaching',
            'computing_time_allocations',
            'observing_proposals',
            'scientific_collaboration_teams',
            'professional_service',
            'references'
            ]
  fp = open('../latex/CV_pub.tex','w')
  add_header(fp)
  fp.write(r"\begin{document}"+'\n')

  add_affiliation(fp)
  for item in itemlist:

    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write('\\newpage\n')

  add_pubheader(fp,header=False,talk=False)

  for item in publist:
    add_pubitem(item,fp)

  add_pubheader(fp,header=False,talk=True)
  # for item in ['invited_review_talks',
  #               'invited_colloquia',
  #               'conference_workshop_seminar_talks']:
  for item in ['professional_presentations']:
    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write(r"\end{document}"+'\n')
  fp.close()

def create_CV_pub_C7():
  itemlist=['education',
            'current_position',
            'employment',
            'grants',
            'research_advising',
            'teaching',
            'computing_time_allocations',
            'observing_proposals',
            'scientific_collaboration_teams',
            'professional_service',
            # 'references'
            ]
  fp = open('../latex/CV_C7.tex','w')
  add_header(fp)
  fp.write(r"\begin{document}"+'\n')

  add_affiliation(fp)
  for item in itemlist:

    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write('\\newpage\n')

  add_pubheader(fp,header=False,talk=False)

  for item in publist:
    add_pubitem(item,fp)

  add_pubheader(fp,header=False,talk=True)
  # for item in ['invited_review_talks',
  #               'invited_colloquia',
  #               'conference_workshop_seminar_talks']:
  for item in ['professional_presentations']:
    if item in items:
      add_item(item,fp)
    else:
      print("cannot find {}.json".format(item))

  fp.write(r"\end{document}"+'\n')
  fp.close()

def create_ref():
  fp = open('../latex/ref.tex','w')
  add_header(fp)
  fp.write(r"\begin{document}"+'\n')

  add_item('references',fp)
  fp.write(r"\end{document}"+'\n')
  fp.close()

if __name__=="__main__":
  create_CV_pub_C7()

