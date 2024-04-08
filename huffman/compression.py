import heapq # pour manipuler le tas

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
            frequency = frequency_dict[key]  #Récupère la fréquence associée au caractère
            binary_tree_node = BinaryTree(key, frequency)  #Crée un nouvel objet BinaryTree (nœud de l'arbre binaire) avec le caractère key et sa fréquence associée frequency.
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
        
    def __build_tree_code_helper(self, root, curr_bit): #root, qui est le nœud actuellement examiné dans l'arbre, et curr_bit, qui est le code binaire actuel en cours de construction
        if root is None:                                  #Vérifie si le noeud actuel (root) est nul.
            return
        if root.caractere is not None:                    # donc c'est une feille 
            self.__code[root.caractere] = curr_bit         #associons le code curr_bit à ce caractère dans le dictionnaire self.__code
            return
        self.__build_tree_code_helper(root.left, curr_bit+'0')  #continuons à explorer récursivement les branches gauche et droite 
        self.__build_tree_code_helper(root.right, curr_bit+'1')
        
    def __build_tree_code(self):
        root = heapq.heappop(self.__heap)  #extrait le nœud racine de l'arbre de Huffman du tas
        self.__build_tree_code_helper(root, '') #chaîne de bits vide 
    
    def __build_encoded_text(self, text):#Pour chaque caractère, concatène au encoded_text le code binaire associé à ce caractère dans le dictionnaire self.__code
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
        return encoded_text
            
    def __build_padded_text(self, encoded_text):
        padding_caractere = 8 - len(encoded_text) % 8 #pour savoir commebien de bits en dois ajouter
        for i in range(padding_caractere):
            encoded_text += '0'       
        padded_info = "{0:08b}".format(padding_caractere)
        padded_text = padded_info + encoded_text
        return padded_text
    
    def compress(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.rstrip()           #supprimer les éventuels espaces ou sauts de ligne à la fin du text
            frequency_dict = self.__frequency_from_text(text)
            self.__build_heap(frequency_dict)
            self.__build_binary_tree()
            self.__build_tree_code()
            encoded_text = self.__build_encoded_text(text) #Construire le texte codé
            padded_text = self.__build_padded_text(encoded_text)
        dictionnary = self.__code
        return dictionnary, padded_text


# Exemple d'utilisation :
# compressed_content, inverse_dictionary = Compression("C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files/fichier 3.txt").compress()
# print("Dictionnaire inversé:", inverse_dictionary)
# print("Contenu compressé:", compressed_content)