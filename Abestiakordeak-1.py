import re
import time
import requests
from selenium import webdriver


def AkordeTxuk(akordeak,pultsu,konpas,ikur,introak):  #Akordeak lista batean sartu introa eta abestia ezberdinduz
    a=[]
    Hasida = False
    for i in range(0,len(akordeak)):
        if Hasida:
            a.append(akordeak[i])
        if akordeak[i]!='   'and akordeak[i]!='af' and akordeak[i]!='Akordeak':
            introak=introak-1
            Hasida=True

        if introak==0:
            a.append('INTROBUKATUA')
            introak=-1

        if i % pultsu == 0:
            a.append(ikur)
            if i % (konpas*pultsu) == 0:
                a.append('\n')
    return a


def Prototipoa(letralista, akordelista):    #Akordearen lista eta Letrak bateratzen ditu
    intro =int( input('Introak zenbat akorde dituen:'))
    m = int(input('Pultsu/konpas:'))
    n = int(input('Konpas:'))
    ikur = str(input('Zerrekin separatu konpasak:'))
    akortxuk = AkordeTxuk(akordelista, m, n, ikur, intro)
    introaegina = False
    j = len(letralista)
    r = 0
    irteera=[]
    for i in range(len(akortxuk)):
        if akortxuk[i] != 'INTROBUKATUA':
            irteera.append(akortxuk[i])
        if akortxuk[i] == 'INTROBUKATUA':
            introaegina = True
            j=i
        if introaegina and r < j+1 and akortxuk[i] == '\n' and i>j:
            irteera.append(letralista[r])
            irteera.append('\n')
            r = r + 1

    return irteera

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

output = ['Akordeak']


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

aktxuk=AkordeTxuk(output,4,4,'|',-1)    #Lortutako akordeak erabiltzaileari erakutsi (ez da beharrezkoa)
for i in range(0,len(aktxuk)):
    print(aktxuk[i],end='')


url = 'https://www.musixmatch.com/es/search/' + abestia #Letra lortu
nav.get(url)
time.sleep(1.5)
elem = nav.find_element_by_css_selector(
    'html.search-results-page.ua-windows_nt.ua-windows_nt-10.ua-windows_nt-10-0.ua-gecko.ua-gecko-79.ua-gecko-79-0.ua-firefox.ua-firefox-79.ua-firefox-79-0.ua-desktop.ua-desktop-windows.js body.has-cookie-alert div#site div#search-results div#content div.search-results div.main-wrapper div div.tab-content div#search-all-results div.main-panel div.box.box-style-plain div.box-content div ul.tracks.list li.showArtist.showCoverart div.track-card.media-card.has-picture div.media-card-body div.media-card-text h2.media-card-title a.title')
elem.click()
time.sleep(1.5)
html = nav.page_source
nav.close()

html=re.sub(r'\n',r' ',html)

letra = re.compile(r',"body":".+","language"')
textua = letra.search(html)

letra = re.sub(r',"body":"','',textua.group())
letra=re.sub(r'","language"',r'',letra)
letra=re.sub(r'\\n',r'\n',letra)
output2=letra.split('\n')

ondodago = False        #Erabiltzailea emaitza errepasatu duela adierazten du

if input('\n\nNahastua? (y)')=='y':         #Erabiltzaileak letra eta akordeak nahasteko aukera ematen du
    Artxiboa = open('C:\\Users\\Usuario\\Documents\\' + abestia + '.txt', 'w')

    while not ondodago:
        buk=Prototipoa(output2,output)
        for i in range(len(buk)):
            print(buk[i],end='')
        ezuz=False
        while not ezuz: #Ikusteko erabiltzailearen erantzuna y edo n izan den
            erantzun=input('\n\n Ondo dago? y/n') #Beharrezkoa bada prozesua errepikatu
            if erantzun == 'y':
                ondodago=True
                ezuz=True
            if erantzun == 'n':
                ezuz=True

    for i in range(len(buk)):
        Artxiboa.write(buk[i])

else:           #Nahasketarik egon ezean bi zatitan gorde
    Artxiboa=open('C:\\Users\\Usuario\\Documents\\'+abestia+'.txt','w')
    for i in range(0, len(output2)):
        Artxiboa.write(output2[i])
        Artxiboa.write('\n\n\n')
    for i in range(0, len(aktxuk)):
        Artxiboa.write(aktxuk[i])



