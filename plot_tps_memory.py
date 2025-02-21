import numpy as np
import os
from matplotlib import pyplot as plt
import csv

#nom coreP coreE coreLPE thread L1 L2 L3
liste_processeur = {
'i9-13900KF_3.00GHz': (8, 16, 0, 32, 49152, 2097152, 37748736),
'Ultra7_155Hx22_AC': (6, 8, 2, 22, 49152, 2097152, 25165824),
'i7-5820K3.30GHz': (6, 0, 0, 12, 65536, 262144, 15728640),
'i7-8650U_1.9GHz_2.11GHz': (4, 0, 0, 16, 65536, 262144, 8388608),
'w10_i5-8400CPU2.80GHz': (6, 0, 0, 6, 65536, 262144, 9437184)
}

def lire_rapport_csv(nom_fichier):
    nbLigne = 0
    nbColonne=0
    tab_data = []
    label = []
    """
    with open(nom_fichier, 'r') as csvfile:
        content = csvfile.read()
    content =  content.replace('\t\n', '\n')        
    with open(nom_fichier, 'w') as csvfile:
        csvfile.write(content)
    """
    with open(nom_fichier, 'r') as csvfile:
        content = csv.reader(csvfile, delimiter='\t')
        for ligne in content:
            if nbColonne==0:
                nbColonne =  len(ligne)
            if nbColonne != len(ligne):
                print("ERREUR ", nom_fichier, nbLigne, nbColonne, len(ligne)    )
            else:
                d = [float(v) for v in ligne]
                tab_data.append(d)
                label.append(d[0])
                nbLigne = nbLigne + 1 
    return tab_data


if os.name == 'nt':
    dossier_rapport = 'c:/lib/build/exempleCUDA/mono_c++11/'
else:
    dossier_rapport = '/home/laurent/build/mono_c++11/'
liste_dossier=[
               './tps_fct_mem_',  './tps_fct_mem_', './tps_fct_mem_',
               './tps_fct_mem_', './tps_fct_mem_'] 
col_use = []
idx = 0
for nom_processeur, nom_dossier in zip(liste_processeur.keys(), liste_dossier):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    tab_data = lire_rapport_csv(nom_dossier + nom_processeur + '.txt')
    print(liste_processeur[nom_processeur][4:])
    x = np.array(tab_data)
    legende = []
    courbe = ax.semilogx(x[:,0]*8*3, x[:,2], marker='+', base=2)
    col_use.append(courbe[0].get_color())
    ax.set_xlabel('Memory size (Byte)')
    ax.set_ylabel('Time/per Byte (s)')
    ax.grid(True)
    ax.legend([nom_processeur])
    taille_cache = liste_processeur[nom_processeur][4:7]
    ax.vlines(taille_cache[0], 0, np.max(x[:,2]), colors=col_use[idx])
    ax.vlines(taille_cache[1], 0, np.max(x[:,2]), colors=col_use[idx])
    ax.vlines(taille_cache[2], 0, np.max(x[:,2]), colors=col_use[idx])
    idx = idx + 1
plt.show()    
