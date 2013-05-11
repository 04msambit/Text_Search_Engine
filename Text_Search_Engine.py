import random
import sys
import re
import os
import collections
import copy
import csv

def boolean_dict(directory):
    path = directory
    dirList=os.listdir(path)
    dictionary=collections.defaultdict(list)
    wordlist=[]
    
    for filename in dirList:
        file = os.path.join(directory, filename)
        f = open(file, 'r')
        for line in f:
            list2=[]
            list2=re.findall(r"[\w']+",line)
            for word in list2:
                w=word.lower()        
                wordlist.append(w)
        
        f.close
        for word in wordlist:
            if dictionary.has_key(word):
               if filename not in  dictionary[word]:
                  dictionary[word].append(filename)
            else:
               dictionary[word]=[filename]
        
        wordlist=[]
    
    return dictionary

def positional_index(directory):
    path = directory
    dirList=os.listdir(path)
    dict_position = {}
    wordlist=[]
    text = []
    tex  = []
    
    for filename in dirList:
        file = os.path.join(directory, filename)
        
        f = open(file, 'r')
        tex=[]
        for line in f:
            list2=[]
            list2=re.findall(r"[\w']+",line)
            for word in list2:
                w=word.lower()
                tex.append(w)

        f.close
        
        text = []
        text = [ element.lower() for element in tex ]
    
            
        #fl.close
        for i in range(0,len(text)):
            #print text[i]
            if text[i] in dict_position:
               if filename in dict_position[text[i]]:
 			dict_position[text[i]][filename].append(i)
               else:
 			dict_position[text[i]][filename]=[i]
               
            else:
               dict_position[text[i]]={}
	       dict_position[text[i]][filename]=[i]
              
    return dict_position


def positional_index_search(dictionary,word):
           
    wordlist=word.split()
    d={} # List of dictionaries
    dlist= []   # The individual dictionaries
    final=[]
    answer=[]

       
    for word in wordlist:
        if word in dictionary:
           d = dictionary[word]
           dlist.append(d)
    # Now we will decrement 
    
    first_dict = dlist[0]
    
    for key in first_dict.keys():
        
        worker_list = [first_dict[key]]
        
        for i in range(1,len(dlist)):
            if key in dlist[i]:
               worker_list.append(dlist[i][key])
                  
        if len(worker_list) == len(wordlist) :
           
           for postn in worker_list[0]:
               count=1
               for j in range(1,len(worker_list)):
                   if (postn+j) in worker_list[j]:
                      count+=1
               if count == len(wordlist):
                  if key not in answer:
                     answer.append(key) 
           
        worker_list=[]
        
    '''del answer[:]
    del worker_list[:]
    del final[:]
    del dlist[:]'''
       
    return answer


def boolean_search(input_dict,input_query):
    word = input_query
    result = []
    if word in input_dict:
       result=input_dict[word]
       
    return result

def wild_card_dictionary(directory):
    path = directory
    dirList=os.listdir(path)
    dictionary_wild_card=collections.defaultdict(list)
    listword=[]
    
    for filename in dirList:
        file = os.path.join(directory, filename)
        f = open(file, 'r')
        for line in f:
            list2=re.findall(r"[\w']+",line)
            for word in list2:
                w=word.lower()
                listword.append(w)
        f.close
        for word in listword:
            string=''
            string= word+'$'
                        
            if word not in dictionary_wild_card:            # We will add a word if it is not always added
               dictionary_wild_card[word]=[]
               for i in range(len(string)):
                   str_val = string[i:]+string[:i]
                   
                   dictionary_wild_card[word].append(str_val)
                           
        
        listword=[]

    return dictionary_wild_card
 
def wild_card_search(main_dict,wild_card_dict,input_query):
    inputword = input_query
    temp_list=[]
    the_lst = []
    result =  []
    string = inputword+'$'
    index  = string.index('*')
    query_string = string[index+1:]+string[:index]   # We do not want * in the query_string
   
    word_bag=[]
    
    for key in wild_card_dict:
        temp_list = []
        temp_list = wild_card_dict[key]
        # We will iterate through all the values to find if it is a part of the substring
        for val in range(len(temp_list)):
            if query_string in temp_list[val]:
               word_bag.append(key)
               break
    for word in word_bag:
        if word in main_dict:
          the_lst.append(main_dict[word])
             
   # Now we need to find the Union of all the elements in the list
    if len(the_lst) !=0:
       result=list(reduce(lambda s1, s2: set(s1) | set(s2), the_lst))
       
    return result

# Provided main(), calls mimic_dict() and mimic()
def main():
 
    flag = 1
    lst=[]
    result=[]
    temporary_list=[]
    final_result=[]
    phrase_list=[]
    text=[]

    boolean=[]
    wild_card=[]
    position_dict=[]
    

    print '\nProcessing started to create the dictionaries...It will take 2-3 minutes...'
  
    boolean = boolean_dict(sys.argv[1])
    position_dict = positional_index(sys.argv[1])
    wild_card = wild_card_dictionary(sys.argv[1])

    print '\nDictionaries created..'

        
    while(flag==1):  
       result = []
       print '\nInput 1: Query 2: Quit'
       inpt = raw_input('\nInput your choice ')
        
       if inpt == '1':
          input_query=''
          input_query = raw_input('\nEnter the Query to be Searched ')
          
          del phrase_list[:]

          phrase_list=re.findall(r'\"(.+?)\"',input_query)
          phrase_list = [ x.lower() for x in phrase_list ]
          
          for phr in phrase_list:
              phr='\"'+phr+'\"'
              input_query=input_query.replace(phr,"")

          del text[:]
          text=input_query.split()
          text = [ x.lower() for x in text ]
       
          for wild in phrase_list:
              lst = positional_index_search(position_dict,wild)
              result.append(lst)

          for qry in text:
              if qry.find('*') !=-1:
                      
                 temporary_list=wild_card_search(boolean,wild_card,qry) 
                 result.append(temporary_list)
              
              else:
                  temporary_list=boolean_search(boolean,qry)       
                  result.append(temporary_list)
          
          if len(result)!=0:
             final_result = []
             final_result=list(reduce(lambda s1, s2: set(s1) & set(s2), result))  
             if len(final_result) !=0 : 
                print 'The query is found in documents'
                print final_result
             else:
                print 'Sorry no match :('
             
          else:
             print 'Sorry no match :('
          
       elif inpt == '2':
            flag = 0
       else:
           print 'Please input correct number'

    print '\nWe will dump the dictionaries to csv files and exit...Dumping Started...'

    w = csv.writer(open("boolean_dict.csv", "w"))
    for key, val in boolean.items():
        w.writerow([key, val])

    w = csv.writer(open("position_dict.csv", "w"))
    for key, val in position_dict.items():
        w.writerow([key, val])

    w = csv.writer(open("wild_card_dict.csv", "w"))
    for key, val in wild_card.items():
        w.writerow([key, val])
    
    
    print '\nDictionaries and Index Files dumped into the Directory path mentioned in command line '
    print '\nThanks..For using the Search Engine...Have a Good Day !!!'
   
  

if __name__ == '__main__':
  main()
