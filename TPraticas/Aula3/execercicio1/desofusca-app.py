import sys
from eVotUM.Cripto import eccblind

settings_file = "./req.settings"

def printUsage():
    print("Usage: python desofusca.py -s <Blind Signature> -RDash <pRDashComponents>")

def load_settings():
    f = open(settings_file, "r")
    blindComponents = f.readline()
    pRComponents = f.readline()
    return blindComponents, pRComponents

def parseArgs():
    if len(sys.argv) == 5 and sys.argv[1] == "-s" and sys.argv[3] == "-RDash":
        main(sys.argv[2], sys.argv[4])
    else:
        printUsage()

def showResults(errorCode, signature):
    print("Output")
    if (errorCode is None):
        print("Signature: %s" % signature) # Imprime a assinatura
    elif (errorCode == 1):
        print("Error: pRDash components are invalid")
    elif (errorCode == 2):
        print("Error: blind components are invalid")
    elif (errorCode == 3):
        print("Error: invalid blind signature format")

def main(blindSignature, pRDashComponents):
    print("Input")
    blindComponents, pRComponents = load_settings() # Carrega do ficheiro do Requerente as components
    errorCode, signature = eccblind.unblindSignature(blindSignature, pRDashComponents, blindComponents)
    showResults(errorCode, signature)

if __name__ == "__main__":
    parseArgs()