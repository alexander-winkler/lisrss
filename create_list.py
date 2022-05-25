from pathlib import Path
import feedparser
import tabulate
import tqdm
import tldextract
    
path = Path.home() / ".newsboat" / "urls"



with open(path, 'r') as IN:
    rows = IN.read().split('\n')
    
lis_rss = []
for r in tqdm.tqdm(rows):
    r = r.split()
    if len(r) > 0:
        try:
            url = r[0]
            if 'LIS' in r[1:]:
                NewsFeed = feedparser.parse(url)
                upd = NewsFeed.get('updated')
                status = NewsFeed.get('status')
                title = NewsFeed.get('feed').get('title')
                lis_rss.append(
                        {
                            'url' : url,
                            'updated' : upd,
                            'status' : status,
                            'title' : title
                            }
                        )

        except Exception as e:
            print(e)

# Sort urls by domain

lis_rss = sorted(lis_rss, key = lambda x:tldextract.extract(x.get('url')).domain)


# Output

with open('Readme.md', 'w') as OUT, open('url_list.csv', 'w') as CSV:
    for x in lis_rss:
        print(x.get('url'), file = CSV)
    with open('Readme_header.md', 'r') as IN:
        OUT.write(IN.read())
    

    header = lis_rss[0].keys()
    rows = [x.values() for x in lis_rss]

    print(tabulate.tabulate(rows, header, tablefmt = 'github' ), file = OUT)
