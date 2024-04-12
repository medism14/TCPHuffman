import heapq # pour manipuler le tas
import os
import json


class BinaryTree:
    
    def __init__(self, carractére, occurence):
        self.carractére = carractére
        self.occurence = occurence
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.occurence < other.occurence
    
class Compression: 
        
    def __init__(self, content, filename):#3
        self.content = content
        self.filename = filename
        self.__heap = []     
        self.__code = {} 
        self.__dictionnaireinversé = {} 
    
    def __lt__(self, other):
        return self.occurence < other.occurence
    
    def __eq__(self, other):
        return self.occurence == other.occurence
        
    def __frequency_from_text(self, text):  

        frequency_dict = {}
        for char in text:
            if char not in frequency_dict:
                frequency_dict[char] = 0
            frequency_dict[char] += 1
        return frequency_dict
        
    def __Build_heap(self, frequency_dict): 
        for key in frequency_dict:
            frequency = frequency_dict[key] 
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node) 
            
    def __Build_Binary_Tree(self):
        while len(self.__heap) > 1: 
            binary_tree_node_1 = heapq.heappop(self.__heap) 
            binary_tree_node_2 = heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.occurence + binary_tree_node_2.occurence
            new_node = BinaryTree(None, sum_of_freq)
            new_node.left = binary_tree_node_1
            new_node.right = binary_tree_node_2
            heapq.heappush(self.__heap, new_node)
        
        
    def __Build_Tree_Code_Helper(self, root, curr_bit):#9
        if root is None:
            return
        if root.carractére is not None: 
            self.__code[root.carractére] = curr_bit
            self.__dictionnaireinversé[curr_bit] =  root.carractére
            return                                          
        self.__Build_Tree_Code_Helper(root.left, curr_bit+'0')
        self.__Build_Tree_Code_Helper(root.right, curr_bit+'1')
        
    def __Build_Tree_code(self):
        root = heapq.heappop(self.__heap) 
        self.__Build_Tree_Code_Helper(root, '') 
     
    
    def __Build_Encoded_Text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
                
        return encoded_text
    
    def __Build_Bite_Array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))
        return array
            
    def __Build_Padded_Text(self , encoded_text):
        padding_carractére = 8 - len(encoded_text) % 8
        for i in range(padding_carractére):
            encoded_text += '0'       
        padded_info = "{0:08b}".format(padding_carractére)
        padded_text = padded_info + encoded_text
        return padded_text
    
    def compress(self): #2
        output_path = f'C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files/{self.filename}' + '.bin'
        frequency_dict = self.__frequency_from_text(self.content)
        self.__Build_heap(frequency_dict)
        self.__Build_Binary_Tree()
        self.__Build_Tree_code()
        encoded_text = self.__Build_Encoded_Text(self.content)
        padded_text = self.__Build_Padded_Text(encoded_text)
        bytes_array = self.__Build_Bite_Array(padded_text)
        final_bytes = bytes(bytes_array)

        with open(output_path, 'wb') as file:
            file.write(final_bytes)

        output_path_dict = f'C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/dictionnaires/{self.filename}' + '.txt'

        dict_str = json.dumps(self.__dictionnaireinversé)

        with open(output_path_dict, 'w', encoding='utf-8') as fileDictionnaire:
            fileDictionnaire.write(dict_str)
        