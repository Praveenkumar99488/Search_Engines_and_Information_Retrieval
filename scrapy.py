from bs4 import BeautifulSoup
import requests
import sys

try:
    if len(sys.argv)<2:
        sys.exit()

    url = sys.argv[1]
    #  I have taken simple browser header to avoid blocking
    headers ={
        "User-Agent":"Mozilla/5.0"
    }
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        try:
            soup=BeautifulSoup(response.content,'html.parser')
            if soup.title:
                print(soup.title.get_text().strip())
            else:
                print()
            if soup.body:
                print(soup.body.get_text().strip())
            else:
                print()
            links=soup.find_all('a')
            for link in links:
                url_link=link.get("href")
                if url_link:
                    print(url_link)
                else:
                    print()
        except Exception as excep:
            print()
    else:
        print()
except Exception as excep:

    print()
