


def separar_cuentos(file):
    """Toma un archivo y devuelve una lista de parrafos donde cada 
    elemento es una lista con las lineas del parrafo"""
    plist=[[]]
    for line in file:
        if len(line)<4:
            #print(line)
            plist.append([line])
        else:
            plist[-1].append(line)
    return plist


def crearcuentos(file):
    """Genera un diccionario con multiples cuentos como objetos (tambien dict)
    con nombre "name", contenido "content", autor "author" y edad "age".
    """
      
    cuentosdict={}
    cuentos=separar_cuentos(file)
    for cuento in cuentos:
        if cuento[1][0:6]=="Catego":
            nameline=2
        else:
            nameline=1
        number=cuento[0][:-1]
        cuentosdict[number]={"name":cuento[nameline], "content":[]}
        for line in cuento[nameline+1:]:
            if line.find("años")==-1 or len(line)>10:
                cuentosdict[number]["content"].append(line)
            else:
                cuentosdict[number]["author"]= cuentosdict[number]["content"].pop()
                cuentosdict[number]["age"]=line
                break
    return cuentosdict

def printtale(cuento):
    print(cuento["name"])
    for line in cuento["content"]:
        print(line[:-1])
    print(cuento["author"])
    print(cuento["age"])
    
    



def printparagraphfile(pars,outputfile='output.txt'):
    """Toma una lista de parrafos (como las que se obtienen de 
    readparagraphs) y guarda en un archivo outputfile el texto original.
    """
    f = open(outputfile, 'w')
    for par in pars:
        for line in par:
            f.write(line)
        f.write('\r\n')
    f.close()


f = open("cuentos.txt", 'r')
cuentos=crearcuentos(f)     

if __name__== "__main__":
    printtale(cuentos["88"])
    printtale(cuentos["90"])

