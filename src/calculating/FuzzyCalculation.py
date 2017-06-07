
'''
Created on 23 de jul de 2016

@author: ErickFlorentino
'''
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

class FuzzyCalculation(object):        
    
    def __init__(self, intensidade_interacoes_AC, intensidade_interacoes_BC, similaridade_entre_vertices, idade_interacoes_AC, idade_interacoes_BC, ShowGraphics = False):
        print intensidade_interacoes_AC, intensidade_interacoes_BC, similaridade_entre_vertices, idade_interacoes_AC,idade_interacoes_BC
        self.intensidade_interacoes_AC = intensidade_interacoes_AC
        self.intensidade_interacoes_BC = intensidade_interacoes_BC
        self.similaridade_entre_vertices = similaridade_entre_vertices
        self.idade_interacoes_AC = idade_interacoes_AC
        self.idade_interacoes_BC = idade_interacoes_BC
        
        # Generate universe variables
        self.x_intensidade_interacoes_AC   = np.arange(0, 100, 1)
        self.x_intensidade_interacoes_BC   = np.arange(0, 100, 1)
        self.x_similaridade_entre_vertices = np.arange(0, 100, 1)
        self.x_idade_interacoes_AC         = np.arange(0, 10, 1)
        self.x_idade_interacoes_BC         = np.arange(0, 10, 1)
        self.x_potencial_ligacao           = np.arange(0, 100, 1)

        # Generate fuzzy membership functions
        self.intensidade_interacoes_AC_baixa   = fuzz.trimf(self.x_intensidade_interacoes_AC, [0, 0, 16])
        self.intensidade_interacoes_AC_media   = fuzz.trimf(self.x_intensidade_interacoes_AC, [8, 16, 24])
        self.intensidade_interacoes_AC_alta    = fuzz.trapmf(self.x_intensidade_interacoes_AC, [16, 24, 35, 35])
        
        self.intensidade_interacoes_BC_baixa   = fuzz.trimf(self.x_intensidade_interacoes_BC, [0, 0, 16])
        self.intensidade_interacoes_BC_media   = fuzz.trimf(self.x_intensidade_interacoes_BC, [8, 16, 24])
        self.intensidade_interacoes_BC_alta    = fuzz.trapmf(self.x_intensidade_interacoes_BC, [16, 24, 100, 100])

        self.similaridade_entre_vertices_baixa = fuzz.trimf(self.x_similaridade_entre_vertices, [0, 0, 50])
        self.similaridade_entre_vertices_medio = fuzz.trimf(self.x_similaridade_entre_vertices, [25, 50, 75])
        self.similaridade_entre_vertices_alta  = fuzz.trimf(self.x_similaridade_entre_vertices, [50, 100, 100])
        
        self.idade_interacoes_AC_baixa         = fuzz.trimf(self.x_idade_interacoes_AC, [0, 1, 1])
        self.idade_interacoes_AC_media         = fuzz.trimf(self.x_idade_interacoes_AC, [0, 1, 2])
        self.idade_interacoes_AC_alta          = fuzz.trimf(self.x_idade_interacoes_AC, [1, 2, 2])
        self.idade_interacoes_BC_baixa         = fuzz.trimf(self.x_idade_interacoes_BC, [0, 1, 1])
        self.idade_interacoes_BC_media         = fuzz.trimf(self.x_idade_interacoes_BC, [0, 1, 2])
        self.idade_interacoes_BC_alta          = fuzz.trimf(self.x_idade_interacoes_BC, [1, 2, 2])
        
        self.potencial_ligacao_baixo           = fuzz.trimf(self.x_potencial_ligacao, [0, 0, 50])
        self.potencial_ligacao_medio           = fuzz.trimf(self.x_potencial_ligacao, [25, 50, 75])
        self.potencial_ligacao_alto            = fuzz.trimf(self.x_potencial_ligacao, [50, 75, 100])
    
    
        self.grau_intensidade_interacoes_AC_baixa   = fuzz.interp_membership(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_baixa, intensidade_interacoes_AC)
        self.grau_intensidade_interacoes_AC_media   = fuzz.interp_membership(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_media, intensidade_interacoes_AC) 
        self.grau_intensidade_interacoes_AC_alta    = fuzz.interp_membership(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_alta, intensidade_interacoes_AC)

        self.grau_intensidade_interacoes_BC_baixa   = fuzz.interp_membership(self.x_intensidade_interacoes_BC, self.intensidade_interacoes_BC_baixa, intensidade_interacoes_BC)
        self.grau_intensidade_interacoes_BC_media   = fuzz.interp_membership(self.x_intensidade_interacoes_BC, self.intensidade_interacoes_BC_media, intensidade_interacoes_BC)
        self.grau_intensidade_interacoes_BC_alta    = fuzz.interp_membership(self.x_intensidade_interacoes_BC, self.intensidade_interacoes_BC_alta, intensidade_interacoes_BC)

        self.grau_similaridade_entre_vertices_baixa = fuzz.interp_membership(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_baixa, similaridade_entre_vertices)
        self.grau_similaridade_entre_vertices_media = fuzz.interp_membership(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_medio, similaridade_entre_vertices)
        self.grau_similaridade_entre_vertices_alta  = fuzz.interp_membership(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_alta, similaridade_entre_vertices)

        self.grau_idade_interacoes_AC_baixa         = fuzz.interp_membership(self.x_idade_interacoes_AC, self.idade_interacoes_AC_baixa, self.idade_interacoes_AC)
        self.grau_idade_interacoes_AC_media         = fuzz.interp_membership(self.x_idade_interacoes_AC, self.idade_interacoes_AC_media, self.idade_interacoes_AC)
        self.grau_idade_interacoes_AC_alta          = fuzz.interp_membership(self.x_idade_interacoes_AC, self.idade_interacoes_AC_alta, self.idade_interacoes_AC)

        self.grau_idade_interacoes_BC_baixa         = fuzz.interp_membership(self.x_idade_interacoes_BC, self.idade_interacoes_BC_baixa, self.idade_interacoes_BC)
        self.grau_idade_interacoes_BC_media         = fuzz.interp_membership(self.x_idade_interacoes_BC, self.idade_interacoes_BC_media, self.idade_interacoes_BC)
        self.grau_idade_interacoes_BC_alta          = fuzz.interp_membership(self.x_idade_interacoes_BC, self.idade_interacoes_BC_alta, self.idade_interacoes_BC)
        
        
        # Generate universe variables
                       
        active_rule1 = np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule1 = np.fmin(active_rule1 ,self.potencial_ligacao_medio)
        print('active_rule1',active_rule1)
        
        active_rule2 = np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule2= np.fmin(active_rule2 ,self.potencial_ligacao_medio)
        print('active_rule2',active_rule2)
        
        active_rule3= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule3= np.fmin(active_rule3,self.potencial_ligacao_alto)
        print('active_rule3',active_rule3)
        
        active_rule4= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule4= np.fmin(active_rule4,self.potencial_ligacao_alto)
        print('active_rule4',active_rule4)
        
        active_rule5= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule5= np.fmin(active_rule5,self.potencial_ligacao_medio)
        print('active_rule5',active_rule5)
        
        active_rule6= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule6= np.fmin(active_rule6,self.potencial_ligacao_alto)
        print('active_rule6',active_rule6)
        
        active_rule7= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule7= np.fmin(active_rule7,self.potencial_ligacao_alto)
        print('active_rule7',active_rule7)
        
        active_rule8= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule8= np.fmin(active_rule8,self.potencial_ligacao_medio)
        print('active_rule8',active_rule8)
        
        active_rule9= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule9= np.fmin(active_rule9,self.potencial_ligacao_baixo)
        print('active_rule9',active_rule9)
        
        active_rule10= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule10= np.fmin(active_rule10,self.potencial_ligacao_baixo)
        print('active_rule10',active_rule10)
        
        active_rule11= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule11= np.fmin(active_rule11,self.potencial_ligacao_baixo)
        print('active_rule11',active_rule11)
        
        active_rule12= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule12= np.fmin(active_rule12,self.potencial_ligacao_alto)
        print('active_rule12',active_rule12)
        
        active_rule13= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule13= np.fmin(active_rule13,self.potencial_ligacao_alto)
        print('active_rule13',active_rule13)
        
        active_rule14= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule14= np.fmin(active_rule14,self.potencial_ligacao_baixo)
        print('active_rule14',active_rule14)
        
        active_rule15= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule15= np.fmin(active_rule15,self.potencial_ligacao_alto)
        print('active_rule15',active_rule15)
        
        active_rule16= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule16= np.fmin(active_rule16,self.potencial_ligacao_alto)
        print('active_rule16',active_rule16)
        
        active_rule17= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule17= np.fmin(active_rule17,self.potencial_ligacao_baixo)
        print('active_rule17',active_rule17)
        
        active_rule18= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule18= np.fmin(active_rule18,self.potencial_ligacao_baixo)
        print('active_rule18',active_rule18)
        
        active_rule19= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule19= np.fmin(active_rule19,self.potencial_ligacao_medio)
        print('active_rule19',active_rule19)
        
        active_rule20= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule20= np.fmin(active_rule20,self.potencial_ligacao_medio)
        print('active_rule20',active_rule20)
        
        active_rule21= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule21= np.fmin(active_rule21,self.potencial_ligacao_baixo)
        print('active_rule21',active_rule21)
        
        active_rule22= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule22= np.fmin(active_rule22,self.potencial_ligacao_medio)
        print('active_rule22',active_rule22)
        
        active_rule23= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule23= np.fmin(active_rule23,self.potencial_ligacao_alto)
        print('active_rule23',active_rule23)
        
        active_rule24= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_alta)))
        potencial_ligacao_rule24= np.fmin(active_rule24,self.potencial_ligacao_medio)
        print('active_rule24',active_rule24)
        
        active_rule25= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule25= np.fmin(active_rule25,self.potencial_ligacao_baixo)
        print('active_rule25',active_rule25)
        
        active_rule26= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule26= np.fmin(active_rule26,self.potencial_ligacao_baixo)
        print('active_rule26',active_rule26)
        
        active_rule27= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule27= np.fmin(active_rule27,self.potencial_ligacao_alto)
        print('active_rule27',active_rule27)
        
        active_rule28= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_baixa ,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule28= np.fmin(active_rule28,self.potencial_ligacao_baixo)
        print('active_rule28',active_rule28)
        
        active_rule29= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_baixa ,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule29= np.fmin(active_rule29,self.potencial_ligacao_medio)
        print('active_rule29',active_rule29)
        
        active_rule30= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_idade_interacoes_BC_baixa ,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule30= np.fmin(active_rule30,self.potencial_ligacao_alto)
        print('active_rule30',active_rule30)
        
        active_rule31= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule31= np.fmin(active_rule31,self.potencial_ligacao_baixo)
        print('active_rule31',active_rule31)
        
        active_rule32= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule32= np.fmin(active_rule32,self.potencial_ligacao_alto)
        print('active_rule32',active_rule32)
        
        active_rule33= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule33= np.fmin(active_rule33,self.potencial_ligacao_alto)
        print('active_rule33',active_rule33)
        
        active_rule34= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule34= np.fmin(active_rule34,self.potencial_ligacao_baixo)
        print('active_rule34',active_rule34)
        
        active_rule35= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule35= np.fmin(active_rule35,self.potencial_ligacao_alto)
        print('active_rule35',active_rule35)
        
        active_rule36= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule36= np.fmin(active_rule36,self.potencial_ligacao_alto)
        print('active_rule36',active_rule36)
        
        active_rule37= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule37= np.fmin(active_rule37,self.potencial_ligacao_alto)
        print('active_rule37',active_rule37)
        
        active_rule38= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule38= np.fmin(active_rule38,self.potencial_ligacao_baixo)
        print('active_rule38',active_rule38)
        
        active_rule39= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule39= np.fmin(active_rule39,self.potencial_ligacao_baixo)
        print('active_rule39',active_rule39)
        
        active_rule40= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule40= np.fmin(active_rule40,self.potencial_ligacao_baixo)
        print('active_rule40',active_rule40)
        
        active_rule41= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule41= np.fmin(active_rule41,self.potencial_ligacao_alto)
        print('active_rule41',active_rule41)
        
        active_rule42= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule42= np.fmin(active_rule42,self.potencial_ligacao_alto)
        print('active_rule42',active_rule42)
        
        active_rule43= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule43= np.fmin(active_rule43,self.potencial_ligacao_medio)
        print('active_rule43',active_rule43)
        
        active_rule44= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule44= np.fmin(active_rule44,self.potencial_ligacao_alto)
        print('active_rule44',active_rule44)
        
        active_rule45= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule45= np.fmin(active_rule45,self.potencial_ligacao_alto)
        print('active_rule45',active_rule45)
        
        active_rule46= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule46= np.fmin(active_rule46,self.potencial_ligacao_alto)
        print('active_rule46',active_rule46)
        
        active_rule47= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule47= np.fmin(active_rule47,self.potencial_ligacao_baixo)
        print('active_rule47',active_rule47)
        
        active_rule48= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule48= np.fmin(active_rule48,self.potencial_ligacao_baixo)
        print('active_rule48',active_rule48)
        
        active_rule49= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule49= np.fmin(active_rule49,self.potencial_ligacao_baixo)
        print('active_rule49',active_rule49)
        
        active_rule50= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule50= np.fmin(active_rule50,self.potencial_ligacao_baixo)
        print('active_rule50',active_rule50)
        
        active_rule51= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule51= np.fmin(active_rule51,self.potencial_ligacao_medio)
        print('active_rule51',active_rule51)
        
        active_rule52= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule52= np.fmin(active_rule52,self.potencial_ligacao_medio)
        print('active_rule52',active_rule52)
        
        active_rule53= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule53= np.fmin(active_rule53,self.potencial_ligacao_baixo)
        print('active_rule53',active_rule53)
        
        active_rule54= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule54= np.fmin(active_rule54,self.potencial_ligacao_medio)
        print('active_rule54',active_rule54)
        
        active_rule55= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule55= np.fmin(active_rule55,self.potencial_ligacao_alto)
        print('active_rule55',active_rule55)
        
        active_rule56= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule56= np.fmin(active_rule56,self.potencial_ligacao_medio)
        print('active_rule56',active_rule56)
        
        active_rule57= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule57= np.fmin(active_rule57,self.potencial_ligacao_alto)
        print('active_rule57',active_rule57)
        
        active_rule58= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_alta,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule58= np.fmin(active_rule58,self.potencial_ligacao_alto)
        print('active_rule58',active_rule58)
        
        active_rule59= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule59= np.fmin(active_rule59,self.potencial_ligacao_alto)
        print('active_rule59',active_rule59)
        
        active_rule60= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule60= np.fmin(active_rule60,self.potencial_ligacao_baixo)
        print('active_rule60',active_rule60)
        
        active_rule61= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule61= np.fmin(active_rule61,self.potencial_ligacao_baixo)
        print('active_rule61',active_rule61)
        
        active_rule62= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule62= np.fmin(active_rule62,self.potencial_ligacao_alto)
        print('active_rule62',active_rule62)
        
        active_rule63= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule63= np.fmin(active_rule63,self.potencial_ligacao_baixo)
        print('active_rule63',active_rule63)
        
        active_rule64= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule64= np.fmin(active_rule64,self.potencial_ligacao_baixo)
        print('active_rule64',active_rule64)
        
        active_rule65= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule65= np.fmin(active_rule65,self.potencial_ligacao_baixo)
        print('active_rule65',active_rule65)
        
        active_rule66= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_AC_media)))
        potencial_ligacao_rule66= np.fmin(active_rule66,self.potencial_ligacao_baixo)
        print('active_rule66',active_rule66)
        
        active_rule67= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule67= np.fmin(active_rule67,self.potencial_ligacao_baixo)
        print('active_rule67',active_rule67)
        
        active_rule68= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule68= np.fmin(active_rule68,self.potencial_ligacao_baixo)
        print('active_rule68',active_rule68)
        
        active_rule69= np.fmin(self.grau_similaridade_entre_vertices_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule69= np.fmin(active_rule69,self.potencial_ligacao_medio)
        print('active_rule69',active_rule69)
        
        active_rule70= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule70= np.fmin(active_rule70,self.potencial_ligacao_baixo)
        print('active_rule70',active_rule70)
        
        active_rule71= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule71= np.fmin(active_rule71,self.potencial_ligacao_baixo)
        print('active_rule71',active_rule71)
        
        active_rule72= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule72= np.fmin(active_rule72,self.potencial_ligacao_medio)
        print('active_rule72',active_rule72)
        
        active_rule73= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_media)))
        potencial_ligacao_rule73= np.fmin(active_rule73,self.potencial_ligacao_baixo)
        print('active_rule73',active_rule73)
        
        active_rule74= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_baixa)))
        potencial_ligacao_rule74= np.fmin(active_rule74,self.potencial_ligacao_baixo)
        print('active_rule74',active_rule74)
        
        active_rule75= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_alta)))
        potencial_ligacao_rule75= np.fmin(active_rule75,self.potencial_ligacao_baixo)
        print('active_rule75',active_rule75)
        
        active_rule76= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule76= np.fmin(active_rule76,self.potencial_ligacao_baixo)
        print('active_rule76',active_rule76)
        
        active_rule77= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule77= np.fmin(active_rule77,self.potencial_ligacao_baixo)
        print('active_rule77',active_rule77)
        
        active_rule78= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule78= np.fmin(active_rule78,self.potencial_ligacao_medio)
        print('active_rule78',active_rule78)
        
        active_rule79= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_baixa)))
        potencial_ligacao_rule79= np.fmin(active_rule79,self.potencial_ligacao_alto)
        print('active_rule79',active_rule79)
        
        active_rule80= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta)))
        potencial_ligacao_rule80= np.fmin(active_rule80,self.potencial_ligacao_baixo)
        print('active_rule80',active_rule80)
        
        active_rule81= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_media)))
        potencial_ligacao_rule81= np.fmin(active_rule81,self.potencial_ligacao_alto)
        print('active_rule81',active_rule81)
        
        active_rule82= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa)))
        potencial_ligacao_rule82= np.fmin(active_rule82,self.potencial_ligacao_baixo)
        print('active_rule82',active_rule82)
        
        active_rule83= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta,self.grau_intensidade_interacoes_AC_alta)))
        potencial_ligacao_rule83= np.fmin(active_rule83,self.potencial_ligacao_baixo)
        print('active_rule83',active_rule83)
        
        active_rule84= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule84= np.fmin(active_rule84,self.potencial_ligacao_baixo)
        print('active_rule84',active_rule84)
        
        active_rule85= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule85= np.fmin(active_rule85,self.potencial_ligacao_baixo)
        print('active_rule85',active_rule85)
        
        active_rule86= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule86= np.fmin(active_rule86,self.potencial_ligacao_alto)
        print('active_rule86',active_rule86)
        
        active_rule87= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule87= np.fmin(active_rule87,self.potencial_ligacao_baixo)
        print('active_rule87',active_rule87)
        
        active_rule88= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule88= np.fmin(active_rule88,self.potencial_ligacao_alto)
        print('active_rule88',active_rule88)
        
        active_rule89= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule89= np.fmin(active_rule89,self.potencial_ligacao_baixo)
        print('active_rule89',active_rule89)
        
        active_rule90= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule90= np.fmin(active_rule90,self.potencial_ligacao_alto)
        print('active_rule90',active_rule90)
        
        active_rule91= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule91= np.fmin(active_rule91,self.potencial_ligacao_medio)
        print('active_rule91',active_rule91)
        
        active_rule92= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule92= np.fmin(active_rule92,self.potencial_ligacao_medio)
        print('active_rule92',active_rule92)
        
        active_rule93= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule93= np.fmin(active_rule93,self.potencial_ligacao_medio)
        print('active_rule93',active_rule93)
        
        active_rule94= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule94= np.fmin(active_rule94,self.potencial_ligacao_alto)
        print('active_rule94',active_rule94)
        
        active_rule95= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule95= np.fmin(active_rule95,self.potencial_ligacao_medio)
        print('active_rule95',active_rule95)
        
        active_rule96= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media, np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_AC_baixa)))
        potencial_ligacao_rule96= np.fmin(active_rule96,self.potencial_ligacao_medio)
        print('active_rule96',active_rule96)
        
        active_rule97= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))
        potencial_ligacao_rule97= np.fmin(active_rule97,self.potencial_ligacao_medio)
        print('active_rule97',active_rule97)
        
        active_rule98= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule98= np.fmin(active_rule98,self.potencial_ligacao_medio)
        print('active_rule98',active_rule98)
        
        active_rule99= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule99= np.fmin(active_rule99,self.potencial_ligacao_baixo)
        print('active_rule99',active_rule99)
        
        active_rule100= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule100= np.fmin(active_rule100,self.potencial_ligacao_baixo)
        print('active_rule100',active_rule100)
        
        active_rule101= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule101= np.fmin(active_rule101,self.potencial_ligacao_baixo)
        print('active_rule101',active_rule101)
        
        active_rule102= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule102= np.fmin(active_rule102,self.potencial_ligacao_medio)
        print('active_rule102',active_rule102)
        
        active_rule103= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule103= np.fmin(active_rule103,self.potencial_ligacao_alto)
        print('active_rule103',active_rule103)
        
        active_rule104= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule104= np.fmin(active_rule104,self.potencial_ligacao_baixo)
        print('active_rule104',active_rule104)
        
        active_rule105= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule105= np.fmin(active_rule105,self.potencial_ligacao_alto)
        print('active_rule105',active_rule105)
        
        active_rule106= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_alta, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule106= np.fmin(active_rule106,self.potencial_ligacao_baixo)
        print('active_rule106',active_rule106)
        
        active_rule107= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_AC_alta)))
        potencial_ligacao_rule107= np.fmin(active_rule107,self.potencial_ligacao_medio)
        print('active_rule107',active_rule107)
        
        active_rule108= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_media,self.grau_intensidade_interacoes_AC_media)))
        potencial_ligacao_rule108= np.fmin(active_rule108,self.potencial_ligacao_medio)
        print('active_rule108',active_rule108)
        
        active_rule109= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule109= np.fmin(active_rule109,self.potencial_ligacao_medio)
        print('active_rule109',active_rule109)
        
        active_rule110= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule110= np.fmin(active_rule110,self.potencial_ligacao_medio)
        print('active_rule110',active_rule110)
        
        active_rule111= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_media, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule111= np.fmin(active_rule111,self.potencial_ligacao_baixo)
        print('active_rule111',active_rule111)
        
        active_rule112= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa ,self.grau_intensidade_interacoes_AC_alta)))
        potencial_ligacao_rule112= np.fmin(active_rule112,self.potencial_ligacao_alto)
        print('active_rule112',active_rule112)
        
        active_rule113= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule113= np.fmin(active_rule113,self.potencial_ligacao_alto)
        print('active_rule113',active_rule113)
        
        active_rule114= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule114= np.fmin(active_rule114,self.potencial_ligacao_alto)
        print('active_rule114',active_rule114)
        
        active_rule115= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_media,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule115= np.fmin(active_rule115,self.potencial_ligacao_baixo)
        print('active_rule115',active_rule115)
        
        active_rule116= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta))))
        potencial_ligacao_rule116= np.fmin(active_rule116,self.potencial_ligacao_alto)
        print('active_rule116',active_rule116)
        
        active_rule117= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_media))))
        potencial_ligacao_rule117= np.fmin(active_rule117,self.potencial_ligacao_baixo)
        print('active_rule117',active_rule117)
        
        active_rule118= np.fmin(self.grau_similaridade_entre_vertices_media, np.fmin(self.grau_idade_interacoes_AC_baixa , np.fmin(self.grau_idade_interacoes_BC_baixa , np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa))))
        potencial_ligacao_rule118= np.fmin(active_rule118,self.potencial_ligacao_medio)
        print('active_rule118',active_rule118)
        
        active_rule119= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule119= np.fmin(active_rule119,self.potencial_ligacao_baixo)
        print('active_rule119',active_rule119)
        
        active_rule120= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule120= np.fmin(active_rule120,self.potencial_ligacao_baixo)
        print('active_rule120',active_rule120)
        
        active_rule121= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule121= np.fmin(active_rule121,self.potencial_ligacao_baixo)
        print('active_rule121',active_rule121)
        
        active_rule122= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule122= np.fmin(active_rule122,self.potencial_ligacao_medio)
        print('active_rule122',active_rule122)
        
        active_rule123= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule123= np.fmin(active_rule123,self.potencial_ligacao_baixo)
        print('active_rule123',active_rule123)
        
        active_rule124= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule124= np.fmin(active_rule124,self.potencial_ligacao_medio)
        print('active_rule124',active_rule124)
        
        active_rule125= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule125= np.fmin(active_rule125,self.potencial_ligacao_medio)
        print('active_rule125',active_rule125)
        
        active_rule126= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule126= np.fmin(active_rule126,self.potencial_ligacao_baixo)
        print('active_rule126',active_rule126)
        
        active_rule127= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_AC_media)))
        potencial_ligacao_rule127= np.fmin(active_rule127,self.potencial_ligacao_baixo)
        print('active_rule127',active_rule127)
        
        active_rule128= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule128= np.fmin(active_rule128,self.potencial_ligacao_baixo)
        print('active_rule128',active_rule128)
        
        active_rule129= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule129= np.fmin(active_rule129,self.potencial_ligacao_baixo)
        print('active_rule129',active_rule129)
        
        active_rule130= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule130= np.fmin(active_rule130,self.potencial_ligacao_medio)
        print('active_rule130',active_rule130)
        
        active_rule131= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_alta,self.grau_intensidade_interacoes_BC_baixa))
        potencial_ligacao_rule131= np.fmin(active_rule131,self.potencial_ligacao_baixo)
        print('active_rule131',active_rule131)
        
        active_rule132= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule132= np.fmin(active_rule132,self.potencial_ligacao_baixo)
        print('active_rule132',active_rule132)
        
        active_rule133= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta,self.grau_idade_interacoes_AC_media)))
        potencial_ligacao_rule133= np.fmin(active_rule133,self.potencial_ligacao_baixo)
        print('active_rule133',active_rule133)
        
        active_rule134= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule134= np.fmin(active_rule134,self.potencial_ligacao_baixo)
        print('active_rule134',active_rule134)
        
        active_rule135= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule135= np.fmin(active_rule135,self.potencial_ligacao_baixo)
        print('active_rule135',active_rule135)
        
        active_rule136= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_alta, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule136= np.fmin(active_rule136,self.potencial_ligacao_medio)
        print('active_rule136',active_rule136)
        
        active_rule137= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule137= np.fmin(active_rule137,self.potencial_ligacao_baixo)
        print('active_rule137',active_rule137)
        
        active_rule138= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule138= np.fmin(active_rule138,self.potencial_ligacao_baixo)
        print('active_rule138',active_rule138)
        
        active_rule139= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule139= np.fmin(active_rule139,self.potencial_ligacao_medio)
        print('active_rule139',active_rule139)
        
        active_rule140= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_media,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule140= np.fmin(active_rule140,self.potencial_ligacao_baixo)
        print('active_rule140',active_rule140)
        
        active_rule141= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule141= np.fmin(active_rule141,self.potencial_ligacao_baixo)
        print('active_rule141',active_rule141)
        
        active_rule142= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule142= np.fmin(active_rule142,self.potencial_ligacao_baixo)
        print('active_rule142',active_rule142)
        
        active_rule143= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule143= np.fmin(active_rule143,self.potencial_ligacao_medio)
        print('active_rule143',active_rule143)
        
        active_rule144= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule144= np.fmin(active_rule144,self.potencial_ligacao_alto)
        print('active_rule144',active_rule144)
        
        active_rule145= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa,self.grau_idade_interacoes_AC_media)))
        potencial_ligacao_rule145= np.fmin(active_rule145,self.potencial_ligacao_alto)
        print('active_rule145',active_rule145)
        
        active_rule146= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule146= np.fmin(active_rule146,self.potencial_ligacao_alto)
        print('active_rule146',active_rule146)
        
        active_rule147= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule147= np.fmin(active_rule147,self.potencial_ligacao_alto)
        print('active_rule147',active_rule147)
        
        active_rule148= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_media, np.fmin(self.grau_intensidade_interacoes_BC_baixa, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule148= np.fmin(active_rule148,self.potencial_ligacao_medio)
        print('active_rule148',active_rule148)
        
        active_rule149= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_alta))
        potencial_ligacao_rule149= np.fmin(active_rule149,self.potencial_ligacao_baixo)
        print('active_rule149',active_rule149)
        
        active_rule150= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_AC_alta)))
        potencial_ligacao_rule150= np.fmin(active_rule150,self.potencial_ligacao_alto)
        print('active_rule150',active_rule150)
        
        active_rule151= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media,self.grau_idade_interacoes_AC_media)))
        potencial_ligacao_rule151= np.fmin(active_rule151,self.potencial_ligacao_alto)
        print('active_rule151',active_rule151)
        
        active_rule152= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_alta))))
        potencial_ligacao_rule152= np.fmin(active_rule152,self.potencial_ligacao_alto)
        print('active_rule152',active_rule152)
        
        active_rule153= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_media))))
        potencial_ligacao_rule153= np.fmin(active_rule153,self.potencial_ligacao_alto)
        print('active_rule153',active_rule153)
        
        active_rule154= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa, np.fmin(self.grau_intensidade_interacoes_BC_media, np.fmin(self.grau_idade_interacoes_AC_baixa ,self.grau_idade_interacoes_BC_baixa ))))
        potencial_ligacao_rule154= np.fmin(active_rule154,self.potencial_ligacao_medio)
        print('active_rule154',active_rule154)
        
        active_rule155= np.fmin(self.grau_similaridade_entre_vertices_baixa, np.fmin(self.grau_intensidade_interacoes_AC_baixa,self.grau_intensidade_interacoes_BC_baixa))
        potencial_ligacao_rule155= np.fmin(active_rule155,self.potencial_ligacao_baixo)
        print('active_rule155',active_rule155)

         # Aggregate all three output membership functions together
         
        aggregated = np.fmax(potencial_ligacao_rule1, potencial_ligacao_rule2)
        aggregated = np.fmax(aggregated, potencial_ligacao_rule3 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule4 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule5 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule6 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule7 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule8 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule9 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule10 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule11 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule12 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule13 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule14 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule15 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule16 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule17 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule18 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule19 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule20 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule21 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule22 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule23 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule24 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule25 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule26 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule27 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule28 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule29 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule30 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule31 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule32 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule33 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule34 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule35 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule36 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule37 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule38 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule39 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule40 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule41 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule42 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule43 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule44 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule45 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule46 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule47 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule48 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule49 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule50 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule51 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule52 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule53 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule54 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule55 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule56 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule57 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule58 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule59 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule60 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule61 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule62 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule63 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule64 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule65 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule66 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule67 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule68 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule69 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule70 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule71 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule72 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule73 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule74 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule75 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule76 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule77 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule78 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule79 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule80 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule81 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule82 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule83 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule84 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule85 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule86 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule87 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule88 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule89 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule90 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule91 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule92 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule93 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule94 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule95 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule96 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule97 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule98 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule99 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule100 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule101 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule102 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule103 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule104 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule105 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule106 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule107 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule108 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule109 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule110 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule111 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule112 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule113 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule114 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule115 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule116 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule117 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule118 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule119 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule120 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule121 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule122 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule123 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule124 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule125 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule126 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule127 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule128 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule129 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule130 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule131 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule132 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule133 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule134 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule135 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule136 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule137 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule138 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule139 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule140 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule141 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule142 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule143 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule144 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule145 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule146 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule147 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule148 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule149 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule150 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule151 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule152 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule153 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule154 )
        aggregated = np.fmax(aggregated, potencial_ligacao_rule155 )
        
            # Calculate defuzzified result
        self.potencial_ligacao = fuzz.defuzz(self.x_potencial_ligacao, aggregated, 'centroid')
       
        self.grau_potencial_ligacao = fuzz.interp_membership(self.x_potencial_ligacao, aggregated, self.potencial_ligacao)
            
        if ShowGraphics:
            fig, ax0 = plt.subplots(figsize=(8, 3))
      
            ax0.plot(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_baixa, 'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_media, 'm', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_intensidade_interacoes_AC, self.intensidade_interacoes_AC_alta, 'r', linewidth=0.5, linestyle='--')
            ax0.set_title('Regra de Intensidade')
                
                
                # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()
      
            plt.tight_layout()
                
            fig, ax0 = plt.subplots(figsize=(8, 3))
      
            ax0.plot(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_baixa, 'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_media, 'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_similaridade_entre_vertices, self.similaridade_entre_vertices_alta, 'r', linewidth=0.5, linestyle='--')
            ax0.set_title('Regra de Similaridade')
                
                
                # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()
      
            plt.tight_layout()
                
      
            fig, ax0 = plt.subplots(figsize=(8, 3))
      
            ax0.plot(self.x_idade_interacoes_AC, self.idade_interacoes_AC_baixa, 'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_idade_interacoes_AC, self.idade_interacoes_AC_media, 'm', linewidth=0.5, linestyle='--', )
            ax0.plot(self.x_idade_interacoes_AC, self.idade_interacoes_AC_alta, 'r', linewidth=0.5, linestyle='--')
            ax0.set_title('Regra de Idade')
                
                
            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()
      
            plt.tight_layout()
      
      
      
            plt.show()