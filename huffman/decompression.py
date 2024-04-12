class Decompression:
    
    def __init__(self, path, dictionnaire):
        self.__path = path
        self.__dictionnaireinversé = dictionnaire

    def __Remove_Padding(self,text):
        padded_info = text[:8]
        padding_carractére = int(padded_info,2)
        text = text[8:]
        text = text[:-1*padding_carractére]
        return text
    
    
    def __Decoded_Text(self,text):#3
        current_bit = ''
        decoded_text = ''
        for char in text:
            current_bit +=char
            if current_bit in self.__dictionnaireinversé:
                decoded_text += self.__dictionnaireinversé[current_bit]  
                current_bit = ''   
        return decoded_text
    
    def decompress(self):#1
        with open(self.__path, 'rb') as file:
            bit_string = ''       
            byte = file.read(1)     
            while byte:
                byte = ord(byte)       
                bits = bin(byte)[2:].rjust(8,'0') 
                bit_string +=bits     
                byte = file.read(1)
               
            text_after_removing_padding = self.__Remove_Padding(bit_string)
            
            actual_text = self.__Decoded_Text(text_after_removing_padding)
        return actual_text  