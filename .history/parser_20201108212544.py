#!/usr/bin/python3

#python3 parser.py input/bible.gedcom > test.txt
import sys
from re import *
from pickle import *
from getopt import getopt



filename = sys.argv[1].split('/')[1]
assetPath = "assets"
indPath = "individuals"
famPath = "families"
cssPath = "assets/gedcom.css"

def gTree(n):
    nome = BG[n]['Name']
    #print(nome)
    for i in BG[n]['Fams']:
        for f in BF[i]['Children']:
            filho = BG[f]['Name'] 
            #print("\t", filho)

def createIndi(ik,iv):
    f = open('assets/individuals/'+ik+'.html', 'w')
    f.write('<h4> <a href=\"../index.html\"> return to index </a> </h4>')
    f.write('<!DOCTYPE html><html><head> <link rel="stylesheet" type="text/css" href="../index.css"></head>\n')
    f.write('<h1> Código do individuo: ' + ik + '</h1>')
    for k, v in iv.items():
        f.write('<b>'+str(k) + ':</b> '+ str(v) + '\n')
    
    nome = BG[ik]['Name']
    f.write(nome)
    for i in BG[ik]['Fams']:
        for j in BF[i]['Children']:
            filho = BG[j]['Name'] 
            f.write("<p> Child: "+ filho+'</p>')
    f.close()

def createFamily(fk,fi):
    f = open('assets/families/'+fk+'.html', 'w')
    f.write('<h4> <a href=\"../index.html\"> return to index </a> </h4>')
    f.write('<!DOCTYPE html><html><head> <link rel="stylesheet" type="text/css" href="../index.css"></head>\n')
    f.write('<h1> Código da familia: ' + fk + '</h1>')
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
        gTree(k)
    for kf,vf in BF.items():  
        createFamily(kf,vf)
    print("\nINDIVIDUOS\n", BG )
    print("\n\n\n\n\n")
    print("\nFAMILIAS\n", BF)
   
    
        
 
    


