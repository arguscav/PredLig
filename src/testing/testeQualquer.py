def reading_files(filename):
    file = open(filename  , 'r')
    data = eval(file.read())
    return data

def converter_calculos():
    file = '/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/data.csv'
    file2 = '/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/data_convertido.csv'
    
    input = reading_files(file)
    
    output = open(file2, 'w')
    
    for item in input:
        output.write(repr(item['node1']))
        output.write(';')
        output.write(repr(item['node2']))
        output.write(';')
        
        output.write(repr(item['cn']))
        output.write(';')
        
        output.write(repr(item['aas']))
        output.write(';')
        
        output.write(repr(item['pa']))
        output.write(';')
        
        output.write(repr(item['jc']))
        output.write(';')
        
        output.write(repr(item['ts08']))
        output.write(';')
        
        output.write(repr(item['ts05']))
        output.write(';')
        
        output.write(repr(item['ts02']))
        output.write('\n')
        
        
    output.close()
    


def converter_analise():
    file = '/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.txt'
    file2 = '/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes_convertido.csv'
    
    input = reading_files(file)
    
    output = open(file2, 'w')
    
    for item in input:
        output.write(repr(item[0]))
        output.write(';')
        output.write(repr(item[1]))
        output.write(';')
        output.write(repr(item[2]))
        output.write('\n')
                
        
    output.close()


if __name__ == '__main__':
    converter_calculos()
    converter_analise()
    
    
    
        
    
        
        
            
   
    
