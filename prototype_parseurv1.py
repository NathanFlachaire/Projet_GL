import subprocess
import os
import sys
from glob import glob


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
        os.system(("pdftotext '%s'") %(path+"/"+fileName))
        abstract=False
        abstractText=""
        found = False
        with open(path+"/"+txtName,"r") as fichier:
            for line in fichier:
                if found == False and ("Abstract" in line or "abstract" in line or "ABSTRACT" in line):
                    abstract=True
                    found = True
                if abstract == True and (len(line) <= 1 or "1 " in line or "I " in line or "1'\n'" in line or "I'\n'" in line or "Keywords" in line or "keywords" in line or "1." in line or "I." in line):
                    abstract = False
                if abstract == True:
                    abstractText += line
        f = open("resumes/resume_"+protoTitle+".txt","w")
        f.write(name+'\n')
        f.write(title[2]+'\n')
        abstractText = abstractText.replace("\n"," ")
        f.write(abstractText+'\n')        

for file in glob('./Papers/*.txt'):
    os.remove(file)