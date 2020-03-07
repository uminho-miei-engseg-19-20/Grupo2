import sys
from eVotUM.Cripto import eccblind
from eVotUM.Cripto import utils

def printUsage():
    print("Usage: python verify.py -cert <certificado do assinante> -msg <mensagem original a assinar> -sDash <Signature> -f <ficheiro do requerente>")

def load_settings(settings_file):
    f = open(settings_file, "r")
    blindComponents = f.readline()
    pRComponents = f.readline()
    return blindComponents, pRComponents

def parseArgs():
    if len(sys.argv) == 9 and sys.argv[1] == "-cert" and sys.argv[3] == "-msg" and sys.argv[5] == "-sDash" and sys.argv[7] == "-f":
        eccPublicKeyPath = sys.argv[2]
        main(eccPublicKeyPath, sys.argv[4], sys.argv[6], sys.argv[8])
    else:
        printUsage()

def showResults(errorCode, validSignature):
    print("Output")
    if (errorCode is None):
        if (validSignature):
            print("Valid signature")
        else:
            print("Invalid signature")
    elif (errorCode == 1):
        print("Error: it was not possible to retrieve the public key")
    elif (errorCode == 2):
        print("Error: pR components are invalid")
    elif (errorCode == 3):
        print("Error: blind components are invalid")
    elif (errorCode == 4):
        print("Error: invalid signature format")

def main(eccPublicKeyPath, data, signature, req_file):
    pemPublicKey = utils.readFile(eccPublicKeyPath) # Leitura do certificado
    blindComponents, pRComponents = load_settings(req_file) # Leitura das componentes
    errorCode, validSignature = eccblind.verifySignature(pemPublicKey, signature, blindComponents, pRComponents, data)
    showResults(errorCode, validSignature)

if __name__ == "__main__":
    parseArgs()