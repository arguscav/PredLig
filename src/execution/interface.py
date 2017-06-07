from execution.arxiv.Step01 import step01
from execution.arxiv.Step02 import step02
from execution.arxiv.Step03 import step03
from execution.arxiv.Step04 import step04
from execution.arxiv.Step05 import step05
from execution.arxiv.Step06 import step06
from execution.arxiv.Step07 import step07
from execution.arxiv.Step08 import step08
from Tkinter import  *
import os.path
import datetime

'''
Created by Andre and Jayme
'''
class StepManager:
    def run(self, i, configFile, neighborhood, runNext, result = ''):
        if( i == 1):
            result += 'Step01 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step01(configFile)
            result += 'Step01 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 2):
            result += 'Step02 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step02(configFile)
            result += 'Step02 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 3):
            result += 'Step03 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step03(configFile, neighborhood)
            result += 'Step03 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 4):
            result += 'Step04 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step04(configFile)
            result += 'Step04 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 5):
            result += 'Step05 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step05(configFile)
            result += 'Step05 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 6):
            result += 'Step06 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step06(configFile)
            result += 'Step06 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        elif( i == 7):
            result += 'Step07 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step07(configFile)
            result += 'Step07 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        else:
            result += 'Step08 started: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
            step08(configFile)
            result += 'Step08 finished: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        
        if( runNext and i < 8):
            result = self.run(i+1, configFile, neighborhood, runNext, result)
        
        return result
            
class Janela:
    def __init__(self, toplevel):
        self.frame = Frame(toplevel)
        self.frame.pack()
        
        self.file_path = 'data/formatado/arxiv/nowell_astroph_1994_1999/config/configuration_forAG.txt'
        self.configFile = 'data/formatado/arxiv/nowell_astroph_1994_1999/config/configuration_forAG.txt'

        #Nao deve conter todas as features mas apenas aquelas que foram escolhidas
        self.featureValues = {}
        
        #o resultado final da linha atualmente colocada como features na verdade agora e scores
        #scores    0:1,0;1:1,0;2:1,0;3:1,0;4:1,0;5:1,0;6:1,0;7:1,0
        #AllFeatures.append(AASFeature())
        #AllFeatures.append(CNFeature())
        #AllFeatures.append(JCFeature())
        #AllFeatures.append(PAFeature())
        #AllFeatures.append(TimeScore())
        #AllFeatures.append(DomainTimeScore())
        #AllFeatures.append(DomainTimeScorevTwo())
        #AllFeatures.append(DomainJC())
        #AllFeatures.append(SPLFeature())
        #AllFeatures.append(LSFeature())
        


        self.parameters = self.getParametersFromFile()
        
          
        self.createContainers()
        self.createForms()
        self.createOptionMenu()
        self.initializeForm()
        self.createStepButtons()
        self.createLogLabel()
        
    '''
    Creates containers
    '''
    def createContainers(self):
        # contains the forms and the buttons for the steps
        self.rootContainerTop=Frame(self.frame)
        self.rootContainerTop.pack(side=TOP)
        
        # contains a label to display messages and a button to erase them
        self.rootContainerBottom=Frame(self.frame)
        self.rootContainerBottom.pack(side=BOTTOM)

        # leftContainer
        self.leftContainer=Frame(self.rootContainerTop)
        self.leftContainer.pack(side=LEFT)

        # container of the forms
        self.formContainer=Frame(self.leftContainer)
        self.formContainer.pack(side=TOP)

        # container for the option menu
        self.optionContainer=Frame(self.leftContainer)
        self.optionContainer.pack(side=BOTTOM)

        # container for the option menu itself
        self.optionLeftContainer=Frame(self.leftContainer)
        self.optionLeftContainer.pack(side=LEFT)

        # container for the option menu text entry and set button
        self.optionRigthContainer=Frame(self.leftContainer)
        self.optionRigthContainer.pack(side=RIGHT)

        # container for the buttons of each step
        self.buttonContainer = Frame(self.rootContainerTop)
        self.buttonContainer.pack(side=RIGHT)
        
    '''
    Create labels and forms and puts them in the right place
    Also creates the save button
    '''
    def createForms(self):
        formWidth = 40
        
        self.myfont = ('Verdana', '10')
        
        
        self.labelName = Label(self.formContainer, text='File name: ',fg='black', font = self.myfont)
        self.name = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelName.grid(row = 0, column = 0)
        self.name.grid(row = 0, column = 1)
    
        self.labelt0 = Label(self.formContainer, text='t0: ',fg='black', font = self.myfont)
        self.t0 = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelt0.grid(row = 1, column = 0)
        self.t0.grid(row = 1, column = 1)
    
        self.labelt0_ = Label(self.formContainer, text='t0_: ',fg='black', font = self.myfont)
        self.t0_ = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelt0_.grid(row = 2, column = 0)
        self.t0_.grid(row = 2, column = 1)
    
        self.labelt1 = Label(self.formContainer, text='t1: ',fg='black', font = self.myfont)
        self.t1 = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelt1.grid(row = 3, column = 0)
        self.t1.grid(row = 3, column = 1)
    
        self.labelt1_ = Label(self.formContainer, text='t1_: ',fg='black', font = self.myfont)
        self.t1_ = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelt1_.grid(row = 4, column = 0)
        self.t1_.grid(row = 4, column = 1)
    
        self.labelDecay = Label(self.formContainer, text='Decay: ',fg='black', font = self.myfont)
        self.decay = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelDecay.grid(row = 5, column = 0)
        self.decay.grid(row = 5, column = 1)
    
        self.labelDomain_decay = Label(self.formContainer, text='Domain Decay: ',fg='black', font = self.myfont)
        self.domain_decay = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelDomain_decay.grid(row = 6, column = 0)
        self.domain_decay.grid(row = 6, column = 1)
    
        self.labelMin_edges = Label(self.formContainer, text='Min_Edges: ',fg='black', font = self.myfont)
        self.min_edges = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelMin_edges.grid(row = 7, column = 0)
        self.min_edges.grid(row = 7, column = 1)
    
        self.labelLengthVertex = Label(self.formContainer, text='LengthVertex: ',fg='black', font = self.myfont)
        self.lengthVertex = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelLengthVertex.grid(row = 8, column = 0)
        self.lengthVertex.grid(row = 8, column = 1)
        
        self.labelNeighborhood= Label(self.formContainer, text='Neighborhood Size: ',fg='black', font = self.myfont)
        self.neighborhood = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelNeighborhood.grid(row = 9, column = 0)
        self.neighborhood.grid(row = 9, column = 1)
        
        
        self.labelScores= Label(self.formContainer, text='Scores: ',fg='black', font = self.myfont)
        self.scores = Entry(self.formContainer, width = formWidth, font = self.myfont)
        self.labelScores.grid(row = 10, column = 0)
        self.scores.grid(row = 10, column = 1)
        
        
        
        # button to save the form
        self.botaoSave = Button(self.formContainer, text="Save")
        self.botaoSave.grid() 
        self.botaoSave.bind("<Button-1>",self.handlerSave)
        
    '''
    Puts the previous parameters(or the placeholders) on the text boxes
    '''
    def initializeForm(self):
        parameters = self.getParametersFromFile()
        self.name.insert(0, parameters['name'])
        self.t0.insert(0, parameters['t0'])
        self.t0_.insert(0, parameters['t0_'])
        self.t1.insert(0, parameters['t1'])
        self.t1_.insert(0, parameters['t1_'])
        self.min_edges.insert(0, parameters['min_edges'])
        self.decay.insert(0, parameters['decay'])
        self.domain_decay.insert(0, parameters['domain_decay'])
        self.scores.insert(0, parameters['scores'])
        self.lengthVertex.insert(0, parameters['lengthVertex'])
    
    def createStepButtons(self):
        self.botao1 = Button(self.buttonContainer, text="Step 01")
        self.botao1.bind("<Button-1>",self.handler01)
        self.botao2 = Button(self.buttonContainer, text="Step 02")
        self.botao2.bind("<Button-1>",self.handler02)
        self.botao3 = Button(self.buttonContainer, text="Step 03")
        self.botao3.bind("<Button-1>",self.handler03)
        self.botao4 = Button(self.buttonContainer, text="Step 04")
        self.botao4.bind("<Button-1>",self.handler04)
        self.botao5 = Button(self.buttonContainer, text="Step 05")
        self.botao5.bind("<Button-1>",self.handler05)
        self.botao6 = Button(self.buttonContainer, text="Step 06")
        self.botao6.bind("<Button-1>",self.handler06)
        self.botao7 = Button(self.buttonContainer, text="Step 07")
        self.botao7.bind("<Button-1>",self.handler07)
        self.botao8 = Button(self.buttonContainer, text="Step 08")
        self.botao8.bind("<Button-1>",self.handler08)
        
        self.runAllTheRest = IntVar()
        self.runAllTheRestCheckBox = Checkbutton( self.buttonContainer, text="Run subsequent steps", variable= self.runAllTheRest)
        
        self.botao1.grid(row = 0, column = 0)
        self.botao2.grid(row = 1, column = 0)
        self.botao3.grid(row = 2, column = 0)
        self.botao4.grid(row = 3, column = 0)
        self.botao5.grid(row = 4, column = 0)
        self.botao6.grid(row = 5, column = 0)
        self.botao7.grid(row = 6, column = 0)
        self.botao8.grid(row = 7, column = 0)
        self.runAllTheRestCheckBox.grid(row = 8, column = 0)

    def createOptionMenu(self):
        formWidth = 20


        
        # nao ta funcionando
        # precisa ver como verifica quando a variavel muda
        # ve com o cara la
        #self.featureVar.trace_variable('w', self.optionChanged())


        
    def createLogLabel(self):
        self.logText = StringVar() 
        self.log = Label(self.rootContainerBottom, textvariable= self.logText,fg='black', font = self.myfont, height=40)
        self.logText.set('Information from processes will appear here')
        self.log.pack()
    '''
    Saves the parameters on the form to one file
    '''
    def saveParametersOnFile(self):
        f = open(self.file_path, 'w+')
        parameters = self.getParametersFromForm()
        # write them lines
        f.write('original_file\tNone\n')
        f.write('graph_file\tdata/formatado/arxiv/' + parameters['name'] + '.txt\n')
        f.write('trainnig_graph_file\tdata/formatado/arxiv/' + parameters['name'] + '/TrainingGraph.txt\n')
        f.write('test_graph_file\tdata/formatado/arxiv/' + parameters['name'] + '/TestingGraph.txt\n')
        f.write('nodes_file\tdata/formatado/arxiv/' + parameters['name'] + '/AllNodes.txt\n')
        f.write('nodes_notlinked_file\tdata/formatado/arxiv/' + parameters['name'] + '/NodesNotLinked.txt\n')
        f.write('calculated_file\tdata/formatado/arxiv/' + parameters['name'] + '/Calculated.txt\n')
        f.write('maxmincalculated_file\tdata/formatado/arxiv/' + parameters['name'] + '/MaxMinCalculated.txt\n')
        f.write('ordered_file\tdata/formatado/arxiv/' + parameters['name'] + '/ordered.txt\n')
        f.write('analysed_file\tdata/formatado/arxiv/' + parameters['name'] + '/analysed.txt\n')
        f.write('t0\t' + parameters['t0'] + '\n')
        f.write('t0_\t' + parameters['t0_'] + '\n')
        f.write('t1\t' + parameters['t1'] + '\n')
        f.write('t1_\t' + parameters['t1_'] + '\n')
        
        
        f.write('decay\t' + parameters['decay'] + '\n')
        f.write('domain_decay\t' + parameters['domain_decay'] + '\n')
        f.write('min_edges\t' + parameters['min_edges'] + '\n')
        f.write('scores\t' + parameters['scores'] + '\n')
        
        
        
        f.write('\n')
        
        self.logText.set('Parameters saved')
        
        f.close()
    
    '''
    Return the parameters from the forms
    '''
    def getParametersFromForm(self):
        parameters = {}
        # parameters from form
        parameters['name'] = self.name.get()
        parameters['t0'] = self.t0.get()
        parameters['t0_'] = self.t0_.get()
        parameters['t1'] = self.t1.get()
        parameters['t1_'] = self.t1_.get()
        parameters['decay'] = self.decay.get()
        parameters['domain_decay'] = self.domain_decay.get()
        parameters['min_edges'] = self.min_edges.get()
        parameters['lengthVertex'] = self.lengthVertex.get()
        parameters['neighborhood'] = self.neighborhood.get()
        parameters['scores'] = self.scores.get()
        
        return parameters
    
    '''
    Recover the parameters from a file
    If file does not exist, create placeholder parameters for the interface
    '''
    def getParametersFromFile(self):
        parameters = {}
        if( os.path.isfile(self.file_path) ):
            f = open(self.file_path, 'r')
            # read first line that is useless i think lol
            line = f.readline()
            # read one line that will give me the name
            line = f.readline()
            parameters['name'] = line[line.rfind('/')+1 : line.find('.txt')]
            # read more useless lines lol
            for i in range(0,7):
                line = f.readline()
            # read useful lines and get the information that is in the format
            # parameter_name parameter_value
            for i in range(0,8):
                line = f.readline()
                parameter_name = line[0:line.find('\t')]
                parameter_value =  line[ line.rfind('\t') + 1 : len(line) - 1]
                parameters[ parameter_name ] = parameter_value
            #for feature in self.features:
                # TODO


            f.close()
        else:
            # if file does not exist, create placeholder for the interface 
            parameters['name'] = "Enter a name"
            parameters['t0'] = "Enter initial time for training graph"
            parameters['t0_'] = "Enter final time for training graph"
            parameters['t1'] = "Enter initial time for testing graph"
            parameters['t1_'] = "Enter final time for testing graph"
            parameters['min_edges'] = "Enter min_edges(TODO)"
            parameters['decay'] = "Enter decay(TODO)"
            parameters['domain_decay'] = "Enter keyword_decay(TODO)"
            parameters['scores'] = "Enter scores "
            
            parameters['lengthVertex'] = "Enter lengthVertex(TODO)"
            
        return parameters
    
    '''
    Event handlers
    handler + i -> step i
    Better to use only one handler for steps and receive the number of the button as a parameter
    It will be done in the future( or it won't) to keep it DRY
    '''
    def handler01(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(1, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step01(self.configFile)
    def handler02(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(2, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step02(self.configFile)
    def handler03(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(3, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #num_people = self.neighborhood.get()
        #step03( self.configFile, int(num_people))
    def handler04(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(4, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step04(self.configFile)
    def handler05(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(5, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step05(self.configFile)
    def handler06(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(6, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step06(self.configFile)
    def handler07(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(7, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step07(self.configFile)
    def handler08(self, event):
        stepManager = StepManager()
        logResult = stepManager.run(8, self.configFile, int(self.getParametersFromForm()['neighborhood']), self.runAllTheRest.get())
        self.logText.set(logResult)
        #step08(self.configFile)
    def handlerSave(self, event):
        self.saveParametersOnFile()    
        
    def featureSetClick(self,event):
        print self.featureValues
        print self.featureEntry.get()
        print self.featureVar.get()
        self.featureValues[ self.featureVar.get() ] = self.featureEntry.get()
        print self.featureValues
        
   
    def optionChanged(self):
        self.featureEntry.delete(0,END)
        self.featureEntry.insert(0, self.featureVar.get())
        
    
#if __name__ == '__main__':
raiz = Tk()
Janela(raiz)
raiz.mainloop()
    
