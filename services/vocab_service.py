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
    
    
    def edit_vocab(self, vocab ,word:str, description:str, example:str, synonums:str, user_id:int, global_flag: int ):
        if user_id != vocab.user_id:
            return "You cannot edit other users vocab"
        if word and word != vocab.word:
            if vocab.id != self._vocab_repository.get_id(word): 
                return "The changed word already exists in database"
            vocab.word = word
        if description:
            if word in description:
                return "Please do not use the vocab word in description"
            vocab.w_description = description
        if example:
            vocab.example = example
        if synonums:
            vocab.synonums = synonums
        if global_flag:
            vocab.global_flag = global_flag        

        self._vocab_repository.edit_vocab(vocab)

    def get_vocab(self,id:int):
        return self._vocab_repository.get_vocab(id)

vocab_service = VocabService()


        