import sys
import requests
import re
from bs4 import BeautifulSoup

B = 53
N = 2**64

def get_text(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.body:
        return soup.body.get_text()
    return ""


def count_words(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)
    freq = {}
    for w in words:
        if w in freq:
            freq[w] =freq[w]+1
        else:
            freq[w] = 1
    return freq


def get_hash(word):
    h=0
    power1=1

    for cha in word:
        h = (h + ord(cha)*power1)%N
        power1 = (power1*B)%N

    return h

def make_simhash(freq):
    bits = [0] * 64
    for word in freq:
        word_hash = get_hash(word)
        count = freq[word]
        for i in range(64):
            if (word_hash >> i) & 1:
                bits[i]=bits[i]+count
            else:
                bits[i]=bits[i]-count

    final=0
    for i in range(64):
        if bits[i]>0:
            final|=(1<<i)
    return final

def same_bits(hash1, hash2):

    xor_value = hash1^hash2
    diff = 0

    while xor_value > 0:
        if xor_value & 1:
            diff=diff+1
        xor_value=xor_value>>1

    return 64-diff


if len(sys.argv) != 3:
    print("Invalid input")
    sys.exit(1)

url1 = sys.argv[1]
url2 = sys.argv[2]

try:
    text1 = get_text(url1)
    text2 = get_text(url2)
    freq1 = count_words(text1)
    freq2 = count_words(text2)
    hash1 = make_simhash(freq1)
    hash2 = make_simhash(freq2)
    result = same_bits(hash1, hash2)

    print("Common bits:", result)

except requests.exceptions.RequestException:
    print("Error loading page")
    sys.exit(1)