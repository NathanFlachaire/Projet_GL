import subprocess
import os
import sys
from glob import glob
import re

if sys.argv[2] == "-x" or sys.argv[2] == "-t":
    if (os.path.isdir("./resumes")):
        os.system(("rm -R '%s'") %("./resumes"))

    command="mkdir resumes"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    path = sys.argv[1]
    for fileName in os.listdir(path):
            name = fileName
            txtName = fileName.replace(".pdf",".txt")
            protoTitle = fileName.replace(".pdf","")
            title = protoTitle.split('_')
            auteur = title[0]
            title = title[2]
            os.system(("pdftotext '%s'") %(path+"/"+fileName))
            titleNext = False
            abstract=False
            abstractText=""
            found = False
            titleFound = False
            auteurToBeFound = False
            auteurFound = False
            titleLine = ""
            auteurLine = ""
            refText =""
            ref = False
            conclusion = False
            with open(path+"/"+txtName,"r") as fichier:
                for line in fichier:
                    line = line.replace("\n","")
                    if titleFound == False and (title.lower() in line.lower() or line.lower() in title.lower()):
                        titleNext = True
                    if auteurFound == False and auteur in line:
                        titleFound = True
                        titleNext = False
                        auteurToBeFound = True
                    if titleNext == True:
                        titleLine = titleLine + line + " "
                    if found == False and "abstract" in line.lower():
                        auteurFound = True
                        auteurToBeFound = False
                        abstract=True
                        found = True
                    if auteurToBeFound == True:
                        auteurLine = auteurLine + line +" "
                    if abstract == True and (len(line) <= 1 or "1 " in line or "I " in line or "1'\n'" in line or "I'\n'" in line or "Keywords" in line or "keywords" in line or "1." in line or "I." in line):
                        abstract = False
                    if abstract == True:
                        abstractText += line
                    if "conclusion" in line.lower():
                        conclusion = True
                    if conclusion == True and ("References" in line or "REFERENCES" in line):
                        ref = True
                    if ref==True:
                        refText+=line

            if sys.argv[2] == "-t":
                f = open("resumes/resume_"+protoTitle+".txt","w")
                f.write(name+'\n'+'\n')
                f.write(titleLine+'\n'+'\n')
                auteurLine = auteurLine.replace("\n"," ")
                f.write(auteurLine+'\n'+'\n')
                abstractText = abstractText.replace("\n"," ")
                abReplace = re.compile(re.escape('abstract'), re.IGNORECASE)
                abstractText = abReplace.sub("Abstract: ",abstractText)
                f.write(abstractText+'\n'+'\n')
                refText = refText.replace("\n"," ")
                refReplace = re.compile(re.escape('references'), re.IGNORECASE)
                refText = refReplace.sub("References: ",refText)
                f.write(refText+'\n')
            else:
                f = open("resumes/resume_"+protoTitle+".xml","w")
                f.write("<article>\n")
                f.write("\t<preamble>"+name+"</preamble>\n")
                f.write("\t<titre>"+titleLine+"</title>\n")
                f.write("\t<auteur>"+auteurLine+"</auteur>\n")
                f.write("\t<abstract>"+abstractText+"</abstract>\n")
                f.write("\t<biblio>"+refText+"</biblio>\n")
                f.write("</article>")

    for file in glob('./Papers/*.txt'):
        os.remove(file)
else:
    print("Argument Invalide")