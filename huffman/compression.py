import heapq

class BinaryTree:
    
    def __init__(self, caractere, occurrence):
        self.caractere = caractere
        self.occurrence = occurrence
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.occurrence < other.occurrence
    
class Compression:
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__dictionnaire_inversé = {}
    
    def __lt__(self, other):
        return self.occurrence < other.occurrence
        
    def __frequency_from_text(self, text):
        frequency_dict = {}
        for char in text:
            if char not in frequency_dict:
                frequency_dict[char] = 0
            frequency_dict[char] += 1
        return frequency_dict
        
    def __build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)
    
    def __build_binary_tree(self):
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap)
            binary_tree_node_2 = heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.occurrence + binary_tree_node_2.occurrence
            new_node = BinaryTree(None, sum_of_freq)
            new_node.left = binary_tree_node_1
            new_node.right = binary_tree_node_2
            heapq.heappush(self.__heap, new_node)
        
    def __build_tree_code_helper(self, root, curr_bit):
        if root is None:
            return
        if root.caractere is not None:
            self.__code[root.caractere] = curr_bit
            self.__dictionnaire_inversé[curr_bit] = root.caractere
            return
        self.__build_tree_code_helper(root.left, curr_bit+'0')
        self.__build_tree_code_helper(root.right, curr_bit+'1')
        
    def __build_tree_code(self):
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root, '')
    
    def __build_encoded_text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
        return encoded_text
    
    def __build_byte_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))
        return array
            
    def __build_padded_text(self , encoded_text):
        padding_caractere = 8 - len(encoded_text) % 8
        for i in range(padding_caractere):
            encoded_text += '0'       
        padded_info = "{0:08b}".format(padding_caractere)
        padded_text = padded_info + encoded_text
        return padded_text
    
    def compress(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.rstrip()
            frequency_dict = self.__frequency_from_text(text)
            self.__build_heap(frequency_dict)
            self.__build_binary_tree()
            self.__build_tree_code()
            encoded_text = self.__build_encoded_text(text)
            padded_text = self.__build_padded_text(encoded_text)
            # bytes_array = self.__build_byte_array(padded_text)
        inverse_dictionary = self.__dictionnaire_inversé
        return inverse_dictionary, padded_text


# Exemple d'utilisation :
# compressed_content, inverse_dictionary = Compression("C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files/fichier 3.txt").compress()
# print("Dictionnaire inversé:", inverse_dictionary)
# print("Contenu compressé:", compressed_content)
