import binascii

class Decompression:
    def __init__(self, dictionnary):
        self.__dictionnary = dictionnary

    def __Remove_Padding(self, text):#2
        padded_info = text[:8]         #extrait les 8 premiers bits du texte
        print(" les 8 premiers bits du texte:",padded_info)
        padding_carractére = int(padded_info,2)         #convertit les 8 bits en entier en base 10
        print("bits de rembourrage ajoutés à la fin du texte compressé:",padding_carractére)
        text = text[8:]                     #supprime les 8 premiers bits du texte
        text = text[:-1*padding_carractére] #supprime les bits de remplissage de la fin du texte
        return text
    
    
    def __Decoded_Text(self,text):#3
        print("Reverse Code Dictionary:",self.__dictionnary) 
        current_bit = ''
        decoded_text = ''
        for char in text:
            current_bit +=char
            if current_bit in self.__dictionnary.values():
                decoded_text += list(self.__dictionnary.keys())[list(self.__dictionnary.values()).index(current_bit)]
                current_bit = ''
        return decoded_text
    
    def decompress(self, padded_text):

        text_after_removing_padding = self.__Remove_Padding(padded_text)
        actual_text = self.__Decoded_Text(text_after_removing_padding)
        
        # print("Dictionnaire inversé: ", self.__dictionnaire_inversé)
        
        return actual_text