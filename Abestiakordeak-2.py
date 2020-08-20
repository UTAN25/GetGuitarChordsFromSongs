import re
import time
import requests
from selenium import webdriver
import pyautogui
import os

def LetraDenbLortu (srtArtxiboa):
    a=[]
    srtArtxiboa=re.sub(r',', r'.', srtArtxiboa)
    itxuraw=re.compile(r'\d\d.(\d\d).(\d\d.\d\d\d).{5}\d\d.(\d\d).(\d\d.\d\d\d)')
    denborak=itxuraw.findall(srtArtxiboa) # gero float bihurtzeko , ak . bihurtu eta goiko formatua bilatu
    letraraw=re.compile(r'[A-Za-z].+')
    letralor=letraraw.findall(srtArtxiboa)
    ta = []
    tb = []
    for i in range(0, len(denborak)):
        ta.append(float(denborak[i][0]) * 60 + float(denborak[i][1]))
        tb.append(float(denborak[i][2]) * 60 + float(denborak[i][3]))


    a.insert(0,letralor)
    a.insert(1,ta)
    a.insert(2,tb)

    return a




abestia =input('Ze abesti bilatu:')

nav = webdriver.Firefox()    #Interneten beharrezko datuak lortu

url = 'https://chordify.net/search/' + abestia
web = requests.get('https://chordify.net/search/', abestia)


nav.get(url)
time.sleep(1.5)
elem = nav.find_element_by_css_selector('.consent-accept-all')
elem.click()
time.sleep(1)
elem = nav.find_element_by_css_selector(
    'html body.searchpage.indexaction.lang-es.user-free.external-referer.user-first.user-intro div#search main.sc-12jjjt7-2.sc-12jjjt7-3.kxAGOS.maincontentspacer div.sc-1hetm98-2.hbbTOt section.sc-10zpxo0-0.efjGBn a.vq90xi-0.vq90xi-1.vq90xi-4.gjhRnV')
elem.click()
time.sleep(1.5)

html = nav.page_source

output = []


interesa = re.compile(r'id="chordsArea".+class="bass-label"></span></div></div><div class="chord"></div>')
irteera = interesa.findall(html)
lista = irteera[0].split('class="bass-label"></span></div></div><div')

for i in range(0, len(lista)):  #Internetetik lortutako datuak txukundu
    lista[i]
    hutsune = re.compile(r'class="chord nolabel"')  #Zati hortan ez daog akorderik
    if hutsune.search(lista[i]) != None:
        output.append('   ')
    else:
        akordeak = re.compile(r'(\w)?\w_maj|(\w)?\w_min')   #Zati horretan akordea dago
        if akordeak.search(lista[i]) != None:
            output.append(akordeak.search(lista[i]).group())
        else:
            output.append('af')  # Akordea falta da

    majkendu = re.compile(r'_maj')  #_maj eta _min aldatu adierazpen egokia lortu
    output[i] = majkendu.sub('  ', output[i])
    minkendu = re.compile(r'_min')
    output[i] = minkendu.sub('m ', output[i])

bideoa=re.compile(r'"(https:\/\/www\.youtube\.com\/watch\?.*?)"')           #Bideoaren linka lortu
url=re.sub(r'"',r'',bideoa.search(html).group(1))

nav.get('https://downsub.com/')
textua = nav.find_element_by_css_selector('#input-31')
textua.send_keys(url)
elementua=nav.find_element_by_css_selector('.mb-5')
elementua.click()
time.sleep(6)
elementua=nav.find_element_by_css_selector('.mt-5 > div:nth-child(1) > button:nth-child(1) > span:nth-child(1) > button:nth-child(2)')
elementua.click()

html2=nav.page_source

time.sleep(6)
pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('Captura2.PNG')))

pyautogui.click(pyautogui.center(pyautogui.locateOnScreen('Captura.PNG')))

nav.close()

path = r"C:\\Users\\Usuario\\Downloads\\"
directories = os.listdir( path )
for i in range(0,len(directories)):
    if re.search(r'.+srt',directories[i]) != None:
        artxiboa=directories[i]

artxiboa='C:\\Users\\Usuario\\Downloads\\'+ artxiboa

with open(artxiboa,'r') as f_open: #byte moduan irakurri errorea ekiditeko
    artx = f_open.read()

os.remove(artxiboa)

a=LetraDenbLortu(artx)

out=[]
j=0
k=0

bidluzeera=re.search(r'Duration: \d\d:(\d\d):(\d\d)',html2)
luzeeraseg=float(bidluzeera.group(1))*60+float(bidluzeera.group(2))

pultso=luzeeraseg/len(output)
print(pultso,'s/akorde')

for t in range(0,len(output)):
    out.append(output[t])
    if j < len(a[1])-1:
        if t*pultso>=a[1][j]-0.2:
            out.append('\n\n')
            j = j + 1

    if k < len(a[2]):
        if t*pultso>=a[2][k]:
            out.append('\n')
            out.append(a[0][k])
            out.append('\n\n')
            k=k+1

for i in range(0,len(out)):
    print(out[i],end='')
