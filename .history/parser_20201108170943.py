#!/usr/bin/python3

#python3 parser.py input/bible.gedcom > test.txt
import sys
from re import *


filename = sys.argv[1].split('/')[1]
assetPath = "assets"
indPath = "individuals"
famPath = "families"
cssPath = "assets/gedcom.css"

def createFamily(fk,fi):
    f = open('assets/families/'+fk+'.html', 'w')
    f.write('<h4> <a href=\"../index.html\"> return to index </a> </h4>')
    f.write('<!DOCTYPE html><html><head> <link rel="stylesheet" type="text/css" href="../index.css"></head>\n')
    f.write('<h1> Código da familia: ' + fk + '</h1>')
    for key,value in fi.items():
        print(key, ":", value)
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
        f.write('<li> <a href=\"'+indPath+'/'+keyi+'.html\">'+keyi+'</a></li>\n')
    f.write('</ul></div></div>')
    f.close()
    
BG = {}
def procIndi(s,i):
    indi = {}
    v = search(r'\bNAME\s+(.*)', i)
    if v:
        indi['name']= v.group(1)
    v = findall (r'\bFAMS\s+@(.*)@',i)
    indi['fams'] = v
    BG[s] = indi 

BF = {}
def procFam(f,i):
    fam={}
    h = search(r'\bHUSB\s+@(.*)@',i)
    if h:
       fam['husb'] = h.group(1)
    w = search(r'\bWIFE\s+@(.*)@',i)
    if w:
        fam['wife'] = w.group(1)
    fam['child'] = findall (r'\bCHIL\s+@(.*)@',i)
    BF[f] = fam
    
    
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
    for k,v in BF.items():
        createFamily(k,v)
        
