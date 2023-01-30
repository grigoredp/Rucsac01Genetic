import random as pyr
import statistics as stats
import matplotlib.pyplot as plt
import threading

# Functie pentru generarea unei liste de valori intregi
def generareLista(lung, a, b):
    temp = []
    for x in range(lung):
        temp.append(pyr.randint(a, b))
    return temp

# Functie pentru generarea cromozomului binar
def generareCrom(lung):
    temp = []
    for x in range(lung):
        temp.append(pyr.choice([0, 1]))
    return temp

# Functie de adecvare
def fitness(crom, date_i):
    (p_valori, p_greutati, limita, lungime) = date_i
    suma_valori = 0
    suma_greutate = 0
    #Se face suma valorilor si a greutatilor cromozomului
    for i, element in enumerate(crom):
        if element == 1:
            suma_greutate = suma_greutate + p_greutati[i]
            suma_valori = suma_valori + p_valori[i]
    if suma_greutate > limita:
        return 0 # Daca depaseste greutatea rucsacului, atunci este 0
    else:
        return suma_valori # Daca nu depaseste, atunci este suma valorilor obiectelor

# Selectia turneu (varianta 1)
def selectieTurneu(populatie_i, date_in, dimensiune_turneu):
    # Lista pentru parintii alesi
    parinti = []

    # Creez o copie a listei populatiei
    populatie = populatie_i[:]
    
    #Se amesteca lista
    pyr.shuffle(populatie)

    # Se face un turneu intre doi cromozomi cu un numar de castigatori 'dimensiune_turneu'
    for x in range(0, dimensiune_turneu*2, 2):
        #print(str(populatie[x])+' f: '+str(fitness(populatie[x], date_in))+" versus "+str(populatie[x+1])+" f: "+str(fitness(populatie[x+1], date_in)))
        if fitness(populatie[x], date_in) > fitness(populatie[x+1], date_in):
            parinti.append(populatie[x])
        else:
            parinti.append(populatie[x+1])

    return parinti

# Selectia turneu 2 (varianta 2)
def selectieTurneu2(populatie_i, date_in, dimensiune_turneu, selectare):
    parinti = []
    for ele in range(selectare):
        temp1 = [] # alegerile
        temp2 = [] # fitness-ul alegerilor
        temp3 = [] # indexul alegerilor in populatie
        for x in range (dimensiune_turneu):
            rc = populatie_i[pyr.choice(range(len(populatie_i)-1))]
            temp1.append(rc)
            temp2.append(fitness(rc,date_in))
            temp3.append(populatie_i.index(rc))
        temp4 = max(temp2) # fitness-ul castigator
        temp5 = temp2.index(temp4) # indexul fitness-ului castigator
        parinti.append(populatie_i[temp5])
    return parinti

# Selectie truncheata
def selectieTruncheata(populatie_i, date_in, lungime):
    temp = sorted(populatie_i, key=lambda i: fitness(i, date_in), reverse=True)
    #print(temp)
    rezultat = []
    for x in range(lungime):
        rezultat.append(temp[x])
    return rezultat

# Incrucisare binara
def incrucisareBinaraSimpla(cr2, cr1, start, stop):
    t1 = cr2[:]
    t2 = cr1[:]
    for i in range(start, stop):
        t2[i], t1[i] = t1[i], t2[i]
    return t1, t2
def generatieUrmatoare(populatie_i, date_in):
    (p_valori, p_greutati, limita, lungime) = date_in
    genUrm = []
    
    populatie = populatie_i[:]
    pop_cop = []
    gen_ales = []

    while len(pop_cop) < round(len(populatie)/3):
        gen_u = []
        
        #sel_crom = selectieTurneu(populatie, date_in, 2)
        sel_crom = selectieTurneu2(populatie, date_in, 2, 2)
        #sel_crom = selectieTruncheata(populatie, date_in, 2)

        if pyr.random() < 0.3:
            gen_u = sel_crom
            #print("fara schimbare")
        else: # Altfel:
            if pyr.random() < 0.6: # Probabilitatea sa se faca o incrucisare
                #print("incrucisare")
                c1, c2 = incrucisareBinaraSimpla(sel_crom[0],sel_crom[1], 0, pyr.randint(1,len(sel_crom[0])-1))
                gen_u.append(c1)
                gen_u.append(c2)
            if pyr.random() < 0.3: # Probabilitatea sa se faca mutatii:
                for i, el in enumerate(gen_u):
                    randn = round(pyr.random(), 2)
                    gen_u[i] = mutatieTare(gen_u[i], randn)
                    #print("mutare"+str(cop)+ " ~ "+str(randn))
        pop_cop.extend(gen_u)
    pop_totala = []
    pop_totala.extend(populatie)
    pop_totala.extend(pop_cop)
    # pop_totala = parinti + copii
    #pop_ales = selectieSample(pop_totala, len(populatie))
    pop_ales = selectieTruncheata(pop_totala,date_in, len(populatie))

    genUrm.extend(pop_ales)
    return genUrm

def selectieSample(pop, lungime):
    return pyr.sample(pop, lungime)

def selectieFitness(pop, lungime, date_intrare):
    temp = pop[:]
    temp = sorted(temp, key=lambda i: fitness(i, date_intrare), reverse=True)
    rezultat = []
    for x in range(lungime):
        rezultat.append(temp[x])
    return rezultat

# Functia de mutatie
def mutatieTare(cr, prob):
    alese = []
    for x in range(len(cr)):
        alese.append(round(pyr.random(), 2))
    #print(str(alese)+" ~ "+str(prob))
    temp = cr[:]
    for i, el in enumerate(alese):
        if el < prob:
            #print(str(temp[i])+ " ~ "+str(1-temp[i]))
            temp[i] = 1- temp[i]
    return temp

# Functie pentru afisarea listei populatiei
def printPopulatie(popi, date_intrare):
    for x in popi:
        print(str(x)+' = ' + str(fitness(x, date_intrare)))

# Functie pentru media unei populatii
def mediePop(popi, di):
    suma = 0
    medie = 0
    for i, el in enumerate(popi):
        suma += fitness(popi[i], di)
    medie = suma/len(popi)
    return medie

# Functiile pentru disperise
def dispersiePop(popi, di):
    fit = []
    for i, el in enumerate(popi):
        fit.append(fitness(popi[i], di))
    disp = stats.variance(fit)*((len(fit)-1)/len(fit))
    return disp
def dispersiePopDeviation(popi, di):
    fit = []
    for i, el in enumerate(popi):
        fit.append(fitness(popi[i], di))
    disp = stats.stdev(fit)
    return disp
def dispersiePopMediana(popi, di):
    fit = []
    for i, el in enumerate(popi):
        fit.append(fitness(popi[i], di))
    disp = stats.median(fit)
    return disp

# Rezolvarea problemei
def rucsac(par_fir, generatii, date_intrare, par_solutii):
    # Crearea unei populatii initiale
    populatie_initiala = []
    for x in range(20):
        populatie_initiala.append(generareCrom(date_intrare[3]))

    # Afisarea pouplatiei initiale 
    def rucPrintPop():
        print("Populatia initala:")
        printPopulatie(populatie_initiala, date_intrare)
        print('')
        print("Media populatiei = "+ str(mediePop(populatie_initiala, date_intrare)))
        print("Varianta (variance) = "+ str(dispersiePop(populatie_initiala, date_intrare)))
        print("Deviatia standard = "+str(dispersiePopDeviation(populatie_initiala, date_intrare)))
        print("Median = "+str(dispersiePopMediana(populatie_initiala, date_intrare)))
    #rucPrintPop()

    px = populatie_initiala[:]
    medie_p = []
    max_optim = populatie_initiala[0]
    max_iter = 0
    plot_iter = []
    plot_disp = []
    for iter in range(generatii):
        plot_iter.append(iter)
        px = generatieUrmatoare(px, date_intrare)

        # Afisarea rezultatelor
        def rucPrintGen():
            print("\n"+"#"+str(iter))
            printPopulatie(px, date_intrare)
            print("Media populatiei = "+ str(mediePop(px, date_intrare)))
            print("Varianta (variance) = "+ str(dispersiePop(px, date_intrare)))
            print("Deviatia standard = "+str(dispersiePopDeviation(px, date_intrare)))
            print("Median = "+str(dispersiePopMediana(px, date_intrare)))
        # rucPrintGen()

        medie_p.append(mediePop(px, date_intrare))
        plot_disp.append(dispersiePopDeviation(px, date_intrare))

        rezultat = sorted(px, key=lambda i: fitness(i, date_intrare), reverse=True)
        if fitness(rezultat[0], date_intrare)>fitness(max_optim, date_intrare):
            max_optim = rezultat[0]
            max_iter = iter
    def rucPrintOptimVechi():
        print("\n"+"Solutie optima dupa "+str(iter)+" iteratii (intalnita prima data):")
        print(str(max_optim)+' = ' + str(fitness(max_optim, date_intrare))+" (iteratia "+str(max_iter)+")")


        rezultat2 = sorted(px, key=lambda i: fitness(i, date_intrare), reverse=True)
        print("\n"+"Solutie optima din ultima generatie (indexul "+str(px.index(rezultat2[0]))+") ")
        print(str(rezultat2[0])+' = ' + str(fitness(rezultat2[0], date_intrare)))
        #rezultat = sorted(px, key=lambda i: fitness(i, date_intrare), reverse=True)
        #print(str(rezultat[0])+' = ' + str(fitness(rezultat[0], date_intrare))+" (index "+str(px.index(rezultat[0]))+")")
    
    #rucPrintOptimVechi()

    def rucPrintRezultatParalel(par_solutii):
        print("Fir: "+str(par_fir)+" | Solutie optima: "+str(max_optim)+' = ' + str(fitness(max_optim, date_intrare))+" (generatia "+str(max_iter)+")")
        rez_temp = [par_fir, max_optim, fitness(max_optim, date_intrare), plot_iter, plot_disp, medie_p]
        par_solutii.append(rez_temp)

    rucPrintRezultatParalel(par_solutii)


    # Datele problemei (pentru testare)
    '''
    crom_valori = [30,15,60,85,100,10,25]
    crom_greutate = [5,14,6,8,14,11,4]

    lungime = 7
    capacitate_rucsac = 30
    '''
    # 30 15 60 85 100 10 25
    # 5 14 6 8 14 11 4
    # Pentru aceste valori solutia optima este
    # Solutie optima: [0, 0, 1, 1, 1, 0, 0] = 245 (iteratia 0)

    # Generarea datelor

def main():
    in_al = 0
    print("Datele sunt introduse manual (0) sau sunt generate (1)?")
    in_al=int(input())
    if in_al == 0:
        print("Care este numarul de obiecte?")
        lungime=int(input())
        print("Care este capacitatea rucsacului?")
        capacitate_rucsac=int(input())
        print("Introduceti numerele separate prin spatiu: ")
        in_man_valori = list(map(int, input("valori: ").strip().split()))[:lungime]
        in_man_greutate = list(map(int, input("greutate: ").strip().split()))[:lungime]

        crom_valori = in_man_valori
        crom_greutate = in_man_greutate
    else:
        print("Care este numarul de obiecte generate?")
        lungime=int(input())
        print("Care este capacitatea rucsacului?")
        capacitate_rucsac=int(input())
        print("Intervalul valorilor obiectelor generate? ? - b (Normal = 1)")
        gen_val_a=int(input())
        print("Intervalul valorilor obiectelor generate? a - ? (Normal = 100)")
        gen_val_b=int(input())
        print("Intervalul greutatii obiectelor generate? ? - b (Normal = 1)")
        gen_gre_a=int(input())
        print("Intervalul greutatii obiectelor generate? a - ? (Normal = 20)")
        gen_gre_b=int(input())

        crom_valori = generareLista(lungime, gen_val_a, gen_val_b)
        crom_greutate = generareLista(lungime, gen_gre_a, gen_gre_b)

    date_intrare = [crom_valori, crom_greutate, capacitate_rucsac, lungime]

    print("Cate fire de executie se folosesc?")
    par_executie=int(input())
    print("Cate generatii se vor obtine?")
    par_gen=int(input())
    par_solutii = []

    # Afisarea datelor de intrare
    print("\n"+str(date_intrare[0])+" - valori")
    print(str(date_intrare[1])+" - greutate")
    print(str(date_intrare[2])+" - capacitatea rucsacului"+"\n")


    print("")

    par_fire =[]

    # Crearea firelor de executie
    for i in range(par_executie):
        par_fire.append(threading.Thread(target=rucsac, args=(i, par_gen, date_intrare, par_solutii)))
        par_fire[i].start()
        # Join este folosit pentru ca firul principal sa astepte terminarea celorlaltor fire.
        par_fire[i].join()

    par_fir_max = 0
    par_fit_max = 0

    # Determinarea solutiei optime
    for i in range(len(par_solutii)):
        if par_solutii[i][2] > par_fit_max:
            par_fir_max = i
            par_fit_max = par_solutii[i][2]

    print()
    print("Solutia finala optima: "+ str(par_solutii[par_fir_max][1]) +" = "+str(par_solutii[par_fir_max][2])+ " din firul "+ str(par_solutii[par_fir_max][0]))


    # Afisarea rezultatelor
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

    for i in range(len(par_solutii)):
        ax1.plot(par_solutii[i][3], par_solutii[i][5], '-', label="Firul "+str(par_solutii[i][0]))
        ax2.plot(par_solutii[i][3], par_solutii[i][4], '-', label="Firul "+str(par_solutii[i][0]))

    ax1.set_title("Media")
    ax2.set_title("Dispersia")
    ax1.legend(loc="best")
    ax2.legend(loc="best")

    plt.tight_layout()
    plt.show()

    temp_quit=input()

if __name__ == "__main__":
    main()