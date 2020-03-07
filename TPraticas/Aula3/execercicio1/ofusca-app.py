import sys
from eVotUM.Cripto import eccblind

settings_file = "./req.settings"

def printUsage():
    print("Usage: python ofusca.py -msg <mensagem a assinar> -RDash <pRDashComponents>")

def parseArgs():
    if len(sys.argv) == 5 and sys.argv[1] == "-msg" and sys.argv[3] == "-RDash":
        main(sys.argv[2], sys.argv[4])
    else:
        printUsage()

def showResults(errorCode, result):
    print("Output")
    if (errorCode is None):
        blindComponents, pRComponents, blindM = result
        print("Blind message: %s" % blindM) # Imprime a blind message no ecra
        f = open(settings_file, "w")
        f.write(blindComponents + "\n" + pRComponents) # Guarda num ficheiro as components
        f.close()
    elif (errorCode == 1):
        print("Error: pRDash components are invalid")

def main(data, pRDashComponents):
    errorCode, result = eccblind.blindData(pRDashComponents, data)
    showResults(errorCode, result)

if __name__ == "__main__":
    parseArgs()