import sys
from eVotUM.Cripto import eccblind

settings_file = "./sig.settings"
initComponents = ""
pRDashComponents = ""

def printUsage():
    print("Usage: python init.py")

def init():
    initComponents, pRDashComponents = eccblind.initSigner()
    f = open(settings_file, "w")
    f.write(initComponents + "\n" + pRDashComponents) # Guarda as componentes no ficheiro settings

def load_settings():
    f = open(settings_file, "r")
    initComponents = f.readline()
    pRDashComponents = f.readline()
    return initComponents, pRDashComponents

def parseArgs():
    if len(sys.argv) == 1: # Programa inicializado sem a opção -init
        initComponents,pRDashComponents = load_settings()
        print("pRDashComponents: %s" % pRDashComponents)
    elif sys.argv[1] == "-init": # Quando inicializado com o -init
        init()
    else:
        printUsage()

if __name__ == "__main__":
    parseArgs()

