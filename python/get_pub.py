import json
import ads
import sys,os


def get_all_papers(author):
    papers = ads.SearchQuery(q='orcid:0000-0003-2896-3725'
                             ' or =author:"{}"'.format(author),
                             sort="date",
                             max_pages=128,
                             fl=["id", "title", "author", "doi", "year",
                                 "pubdate", "pub", "volume", "issue", "page",
                                 "identifier", "doctype", "citation_count",
                                 "bibcode"])

    all_dicts = []
    for paper in papers:
        # Get arxiv ID
        aid = [":".join(t.split(":")[1:]) for t in paper.identifier
               if t.startswith("arXiv:")]

        try:
            page = int(paper.page[0])
        except (ValueError, TypeError):
            page = None
            if paper.page is not None and paper.page[0].startswith("arXiv:"):
                aid.append(":".join(paper.page[0].split(":")[1:]))

        title = paper.title[0]
        if '<SUB>' in title:
            title=title.replace('<SUB>','').replace('</SUB>','')
        if 'α' in title:
            title=title.replace('α','-alpha')

        all_dicts.append(dict(
            doctype=paper.doctype,
            authors=paper.author,
            year=paper.year,
            pubdate=paper.pubdate,
            doi=paper.doi[0] if paper.doi is not None else None,
            title=title,
            pub=paper.pub,
            volume=paper.volume,
            issue=paper.issue,
            page=page,
            arxiv=aid[0] if len(aid) else None,
            citations=(paper.citation_count
                       if paper.citation_count is not None else 0),
            url="http://adsabs.harvard.edu/abs/" + paper.bibcode,
        ))

    return sorted(all_dicts, key=lambda x: x['pubdate'], reverse=True)


if __name__ == '__main__':
    papers = get_all_papers("Kim,Chang-Goo")

    dirpath = os.path.dirname(__file__)

    with open(os.path.join(dirpath,"..","data","pubs.json"), "w") as f:
        json.dump(papers, f, sort_keys=True,
                  indent=4, separators=(",", ": "))

    # option for korean jobs
    if len(sys.argv) > 1:
        i=1
        output=[]
        for p in papers:
            if p['doctype']=='article':
                out=[]
                out.append('{:d}'.format(i))
                out.append('SCIE')
                out.append(''.join(p['pubdate'].split('-')[:-1]))
                title = '"{0}"'.format(p['title'])
                out.append(title)
                out.append(' ')
                out.append(' ')
                out.append(' ')
                out.append(p['pub'])
                if 'Astrophysical Journal' in p['pub']:
                    out.append('IOP Publishing')
                    out.append('1538-4357')
                elif 'Monthly' in p['pub']:
                    out.append('Oxford University Press')
                    out.append('1365-2966')
                else:
                    out.append('Null')
                    out.append('Null')
                out.append('{:d}'.format(len(p['authors'])))
                out.append(p['volume'])
                if p['issue'] != None:
                    out.append(p['issue'])
                else:
                    out.append(' ')
                if p['page'] != None:
                    out.append('{:d}'.format(p['page']))
                else:
                    out.append(' ')
                out.append(' ')
                out.append(' ')
                out.append(p['doi'])
                out.append('\n')
                output.append(','.join(out))
                i+=1
        with open('yonsei.csv','w') as fp:
            for out in output:
                fp.write(out)
