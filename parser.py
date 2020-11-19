#!/usr/bin/python3

#python3 parser.py input/bible.gedcom > test.txt
import sys
from re import *
from pickle import *
from getopt import getopt

filename = sys.argv[1].split('/')[1]
indPath = "individuals"
famPath = "families"


def createIndi(ik,iv):
    wife = husband = wn = hn = ""
    f = open('assets/individuals/'+ik+'.html', 'w')
    f.write('<!DOCTYPE html>\n<html>\n<head>\n\t<title>'+ik+'</title>\n\t<link rel="stylesheet" type="text/css" href="../index.css">\n</head>\n')
    f.write('<body>\n')
    f.write('\t<h4><a href=\"../index.html\"> return to index</a></h4>\n')
    f.write('\t<h1>Individuo: ' + ik + '</h1>\n')

    for k, v in iv.items():
        f.write('\t<b>'+str(k) + ':</b> '+ str(v) + ' <br>\n')

    f.write('\t<div class="tree">\n\t\t<ul>\n\t\t\t<li>\n')

    for i in BG[ik]['Fams']:
        if 'Wife' in BF[i]:
            wife = BF[i]['Wife']
            wn = BG[wife]['Name']
        if 'Husband' in BF[i]:
            husband = BF[i]['Husband']
            hn = BG[husband]['Name']
        f.write('\t\t\t\t<a href="#'+'">'+ wn + ' & ' + hn + '</a>\n')
        f.write('\t\t\t\t<ul>\n')

        for j in BF[i]['Children']:
            filho = BG[j]['Name'] 
            f.write('\t\t\t\t\t<li><a href="'+j+'.html">'+ filho +'</a></li>\n')

        f.write('\t\t\t\t</ul>\n')

    f.write('\t\t\t</li>\n\t\t</ul>\n\t</div>\n')
    f.write('</body>\n</html>')
    f.close()

def createFamily(fk,fi):
    f = open('assets/families/'+fk+'.html', 'w')
    f.write('<h4> <a href=\"../index.html\"> return to index </a> </h4>')
    f.write('<!DOCTYPE html><html><head> <link rel="stylesheet" type="text/css" href="../index.css"></head>\n')
    f.write('<h1> Familia: ' + fk + '</h1>')
    for k, v in fi.items():
       f.write('<b>'+str(k) + ':</b> '+ str(v) +'\r\n')
    f.close()

def createIndex(fam,indi):
    f = open("assets/index.html", 'w')
    f.write('<!DOCTYPE html><html><head> <link rel="stylesheet" type="text/css" href="index.css"></head>\n')
    f.write('<h1> Ficheiro: ' + filename + '</h1>')
    f.write('<div class="row"><div class="column"><h2>Familias</h2>')
    for keyf in fam:
        f.write('<li> <a href=\"'+famPath+'/'+keyf+'.html\">'+keyf+'</a></li>\n')
    f.write('</ul> </div>')
    f.write('<div class="column"><h2>Individuos</h2>')
    for keyi in indi:
        f.write('<li> <a href=\"'+indPath+'/'+keyi+'.html\">'+BG[keyi]['Name']+'</a></li>\n')
    f.write('</ul></div></div>')
    f.close()

#contruir um individuo e as suas carateristicas
BG = {}
def procIndi(s,i):
    indi = {}
    name = search(r'\bNAME\s+(.*)', i)
    title = search(r'\bTITL\s+(.*)', i)
    gender = search(r'\bSEX\s+(.*)', i)
    if name:
        indi['Name']= name.group(1)
    fams = findall (r'\bFAMS\s+@(.*)@',i)
    indi['Fams']= fams
    if title:
        indi['Title'] = title.group(1)
    if gender:
        indi['Gender'] = gender.group(1)
    BG[s] = indi 
    

BF = {}
def procFam(f,i):
    fam={}
    h = search(r'\bHUSB\s+@(.*)@',i)
    if h:
       fam['Husband'] = h.group(1)
    w = search(r'\bWIFE\s+@(.*)@',i)
    if w:
        fam['Wife'] = w.group(1)
    fam['Children'] = findall (r'\bCHIL\s+@(.*)@',i)
    BF[f] = fam
    #print(fam['Children'])
    
    
def process(t):
    items = split(r'\n0',t) 
    for i in items: 
        z = search(r'@(I\d+)@ *INDI', i) #procura todos os individuos
        if z: 
            procIndi(z.group(1),i)
        f = search(r'@(F\d+)@ *FAM', i) #procura todas as familias 
        if f:
            procFam(f.group(1),i)


with open(sys.argv[1], 'r') as f :
    gedcom = f.read()
    process(gedcom)
    createIndex(BF.keys(), BG.keys())
    for k,v in BG.items():
        createIndi(k,v)
    for kf,vf in BF.items():  
        createFamily(kf,vf)
    #print("\nINDIVIDUOS\n", BG )
    #print("\n\n\n\n\n")
    #print("\nFAMILIAS\n", BF)
   
    
        
 
    


