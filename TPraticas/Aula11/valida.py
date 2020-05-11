from datetime import datetime
import re
import string



#--------------------------------------------------------------------------#
#-------------------FUNÇÃO QUE VALIDA O VALOR A PAGAR----------------------#
#--------------------------------------------------------------------------#
# Verifica, através da expressão regular abaixo, as seguintes regras:
# -------> Se o valor é maior que 0.0
# -------> Se um valor decimal é da forma _.02 ou _.20, não pondendo ser _.2
# INPUT: Valor a pagar
# OUTPUT: True, se for válido. False, caso contrário.
def validaValor(valor):

    try: 

        match = re.match(r'^((0?\.((0[1-9])|[1-9]\d))|([1-9]\d*(\.\d{2})?))', valor) 
     

    except ValueError:

         return False

    else: 

         if (match is not None) and (len(valor) < 9):
             return True

         else:
             return False




#--------------------------------------------------------------------------#
#------------FUNÇÃO QUE VALIDA UMA DATA CONFORME O SEU TIPO----------------#
#--------------------------------------------------------------------------#
# Caso seja uma data de nascimento, é esperado que esta seja anterior à atual.
# Caso contrário, que é o caso da data de validade do cartão de crédito,
# é suposto que este seja posterior à data atual.
# INPUT: data e o tipo de data.
# OUTPUT: True, se for válida. False, caso contrário.
def validaData(dataa, tipoData):

    try:
        # verifica se tem o formato pretendido
        data = datetime.strptime(dataa, "%Y-%m-%d")


    except ValueError:

         return False

    else: 

        dataAtual = datetime.now()

 
        if tipoData is "dataNascimento" :
                 # verifica se a data de nascimento é anterior à data atual
                 if (dataAtual > data):

                    return True

                 else:
                    return False



        else:  # é porque é dataCartao
                 if  (dataAtual < data):
                     return True
                 else:
                     return False
    




#--------------------------------------------------------------------------#
#-----------------------FUNÇÃO QUE VALIDA UM NOME--------------------------#
#--------------------------------------------------------------------------#
# Verifica, através da expressão regular abaixo, se o nome colocado não
# apresenta nenhum caractere especial, podendo apenas ser composta por letras
# e espaços.
# Definiu-se o tamanho do nome com o máximo de 50 caracteres e o mínimo de 7.
# INPUT: Nome.
# OUTPUT: True, se for válido. False, caso contrário.
def validaNome(nome):

    try: 

        match = re.match(r'^[a-zA-Z]+(([ ][a-zA-Z ])?[a-zA-Z]*)*$', nome) 
     

    except ValueError:

         return False

    else: 

         if (match is not None) and (len(nome) < 50) and (len(nome) > 7) :
             return True

         else:
             return False
       




# Reutilizou-se o código encontrado em https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf?fbclid=IwAR2Hy0UtJKj6RhedMeBB4t8MrjAJIjtY_kyFrA_FkkLmqsYFC2zX2FiY94Y
def _toIntList(numstr, acceptX=0):
    """
    Converte string passada para lista de inteiros,
    eliminando todos os caracteres inválidos.
    Recebe string com nmero a converter.
    Segundo parÃ¢metro indica se 'X' e 'x' devem ser
    convertidos para '10' ou não.
    """
    res = []

    # converter todos os dígitos
    for i in numstr:
        if i in string.digits:
            res.append(int(i))

    # converter dígito de controlo no ISBN
    if acceptX and (numstr[-1] in 'Xx'):
        res.append(10)
    return res


# Reutilizou-se o código encontrado em https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf?fbclid=IwAR2Hy0UtJKj6RhedMeBB4t8MrjAJIjtY_kyFrA_FkkLmqsYFC2zX2FiY94Y
def _valN(num):
    """
    Algoritmo para verificar validade de NIF.
    Recebe string com número a validar.
    """

    # converter num (string) para lista de inteiros
    num = _toIntList(num)

    # computar soma de controlo
    sum = 0
    for pos, dig in enumerate(num[:-1]):
        sum += dig * (9 - pos)

    # verificar soma de controlo
    return (sum % 11 and (11 - sum % 11) % 10) == num[-1]




#--------------------------------------------------------------------------#
#-------------------FUNÇÃO QUE VALIDA UM NIF OU UM NIC---------------------#
#--------------------------------------------------------------------------#
# Verifica se o tamanho do número é 9 e se o primeiro digito não é 0.
# INPUT: Nif ou Nic.
# OUTPUT: True, se for válido. False, caso contrário.
# Reutilizou-se o código encontrado em https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf?fbclid=IwAR2Hy0UtJKj6RhedMeBB4t8MrjAJIjtY_kyFrA_FkkLmqsYFC2zX2FiY94Y
def validaNif_Nic(nr):
    """
    Verifica validade de número de contribuinte.
    Recebe string com NIF.
    """

    # verificar tamanho do número passado
    if len(nr) != 9:
        return False

    # verificar validade do carácter inicial do NIF
    if nr[0] not in "125689":
        return False

    # verificar validade
    return _valN(nr)





#--------------------------------------------------------------------------#
#-------------------FUNÇÃO QUE VALIDA O NÚMERO DE UM CC--------------------#
#--------------------------------------------------------------------------#
# Verifica se o número está conforme os parâmetros.
# INPUT: Número de um cartão de crédito.
# OUTPUT: True, se for válido. False, caso contrário.
# Reutilizou-se o código encontrado em https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf?fbclid=IwAR2Hy0UtJKj6RhedMeBB4t8MrjAJIjtY_kyFrA_FkkLmqsYFC2zX2FiY94Y
def validaNrCartao(ncc):

    """
    Verifica a validade de número de cartão de crédito.
    Recebe string com número do cartão de crédito.
    """

    # converter número para lista de inteiros e inverter lista
    ncc = _toIntList(ncc)
    ncc.reverse()

    # verificar tamanho do número
    if 7 > len(ncc) or len(ncc) > 19:
        return False

    # computar soma de controlo
    sum = 0
    alt = False

    for i in ncc:
        if alt:
            i *= 2
            if i > 9:
                i -= 9
        sum += i
        alt = not alt

    # verificar soma de controlo
    return not (sum % 10)





#--------------------------------------------------------------------------#
#-------------------FUNÇÃO QUE VALIDA O CVC DE UM CC-----------------------#
#--------------------------------------------------------------------------#
# Verifica se o CVC tem exatamente três digitos.
# INPUT: CVC.
# OUTPUT: True, se for válido. False, caso contrário.
def validaCVC(cvc):

    try: 

        match = re.match(r'[0-9][0-9][0-9]', cvc) 
     

    except ValueError:

         return False

    else: 

         if (match is not None) :
             return True

         else:
             return False




             

def main():

        print("-------------------------------------------------------------------------")
        print("------------------Insira os seguintes dados, por favor:------------------")
        print("-------------------------------------------------------------------------")


        print("\n")
        valor = input('Valor a pagar: ')

        while(validaValor(valor) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!!O valor que colocou é inválido. Insira, de novo, por favor!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            valor = input('Valor a pagar: ')



        print("\n")
        data = input('Data de nascimento, no formato YYYY-M-D: ')

        
        while(validaData(data, "dataNascimento") is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!A data que colocou é inválida. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            data = input('Data de nascimento, no formato YYYY-M-D: ')


        print("\n")
        nome = input('Nome: ')

        
        while(validaNome(nome) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!O nome que colocou é inválido. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            nome = input('Nome: ')


        print("\n")
        nif = input('NIF: ')

        
        while(validaNif_Nic(nif) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!O NIF que colocou é inválido. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            nif = input('NIF: ')


        print("\n")
        nic = input('NIC: ')

        
        while(validaNif_Nic(nic) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!O NIC que colocou é inválido. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            nif = input('NIC: ')



        print("\n")
        ncc = input('Número do cartão de crédito: ')

        
        while(validaNrCartao(ncc) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!O nr do CC que colocou é inválida. Insira, de novo, por favor!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ncc = input('Número do cartão de crédito: ')


        print("\n")
        dataC = input('Data de validade do cartão de crédito: ')

        
        while(validaData(dataC, "dataCartao") is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!A data que colocou é inválida. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            dataC = input('Data de validade do cartão de crédito: ')


        print("\n")
        cvc = input('CVC: ')

        
        while(validaCVC(cvc) is False):
            print("\n")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!!!!!!O CVC que colocou é inválida. Insira, de novo, por favor.!!!!!!!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            cvc = input('CVC: ')


        print("\n")

        print("-------------------------------------------------------------------------")
        print("--------------------Obrigada pelo preenchimento!-------------------------")
        print("-------------------------------------------------------------------------")




main()
