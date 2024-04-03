import binascii

class Decompression:
    def __init__(self, dictionnaire_inversé):
        self.__dictionnaire_inversé = dictionnaire_inversé

    def __Remove_Padding(self,text):#2
        padded_info = text[:8]         #extrait les 8 premiers bits du texte
        print(" les 8 premiers bits du texte:",padded_info)
        padding_carractére = int(padded_info,2)         #convertit les 8 bits en entier en base 10
        print("bits de rembourrage ajoutés à la fin du texte compressé:",padding_carractére)
        text = text[8:]                     #supprime les 8 premiers bits du texte
        text = text[:-1*padding_carractére] #supprime les bits de remplissage de la fin du texte
        return text
    
    
    def __Decoded_Text(self,text):#3
        print("Reverse Code Dictionary:", self.__dictionnaire_inversé) 
        current_bit = ''
        decoded_text = ''
        for char in text:
            current_bit +=char
            #print("current_bit:", current_bit)
            if current_bit in self.__dictionnaire_inversé:
                decoded_text += self.__dictionnaire_inversé[current_bit]  
                current_bit = ''   
        return decoded_text

    def decompress(self, padded_text):


        text_after_removing_padding = self.__Remove_Padding(padded_text)
        actual_text = self.__Decoded_Text(text_after_removing_padding)
        
        # print("Dictionnaire inversé: ", self.__dictionnaire_inversé)
        # print("Compressed bytes: ", compressed_content)
        # print("Padded text: ", padded_text)

        return actual_text