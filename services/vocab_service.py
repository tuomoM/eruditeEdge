from repositories.vocab_repository import VocabRepository
from repositories.vocab_repository import vocab_repository as default_vocab_repository


class VocabService:
    def __init__(self,vocab_repository:VocabRepository = default_vocab_repository )-> None:
        self._vocab_repository = vocab_repository

    def add_vocab(self, word: str,description: str, example: str, synonums: str, user_id:int):
        if not word:
            return "Please input a vocab word"
        if not description:
            return "Please input description"
        if word in description:
            return "Please do not use the vocab word in description"
        if not example:
            return "Please input example where word is used"
        if not synonums:
            return "Please input synonyms for word:" + word
        if self._vocab_repository.vocab_exists(word):
            return "Word already exists in database"
        self._vocab_repository.save_vocabs(word,description,example,synonums,user_id)

    def get_vocabs(self,user_id):
        return self._vocab_repository.get_vocabs(user_id)
    
    
    def edit_vocab(self, vocab ,word:str, description:str, example:str, synonyms:str, global_flag: int ):
        id = vocab["id"]
        if description:
            if word in description:
                return "Please do not use the vocab word in description"
                

        self._vocab_repository.edit_vocab(word, description, example, synonyms, global_flag, id)

    def get_vocab(self,id:int):
        return self._vocab_repository.get_vocab(id)
    
    def delete_vocab(self, vocab_id):
       return_value = self._vocab_repository.del_vocab(vocab_id)
       if return_value: 
          return return_value 
       
    def find_by_word(self, search_string, user_id):
        return self._vocab_repository.find_vocabs(search_string,user_id)

vocab_service = VocabService()


        