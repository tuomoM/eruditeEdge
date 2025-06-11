from repositories.vocab_repository import VocabRepository
from repositories.vocab_repository import vocab_repository as default_vocab_repository
import hashlib, time


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
    
  
    def get_vocabset(self,user_id:int, ids):
        return self._vocab_repository.get_vocabs_by_ids(user_id, ids)
        
    def generate_hash(self,vocab_ids):
        vocab_ids_copy = vocab_ids[:]
        vocab_ids_copy.sort()
        vocab_ids_str = ','.join(map(str, vocab_ids_copy))
        hash_value = hashlib.sha256(vocab_ids_str.encode()).hexdigest()
    
        return hash_value
    def get_training_id(self,user_id, vocab_ids):
        vocab_hash = self.generate_hash(vocab_ids)
        id = self._vocab_repository.get_training_id(user_id,vocab_hash)
        if id == None:
            result = self.save_training(user_id,vocab_ids, vocab_hash)
            return result
        else:
            return id

    def save_training(self, user_id, vocab_ids, vocab_hash):
        time_stamp = time.time()
        training_id = self._vocab_repository.save_training(user_id,vocab_hash,time_stamp,vocab_ids)
        return training_id
    
    def check_answers(self,training_id, answers):
        correct_answers = self._vocab_repository.get_answers(training_id)
        results = []
        for vocab in correct_answers:
            vocab_id = vocab["id"]
            correct_word = vocab["word"]
            description = vocab["w_description"]
            user_answer = answers.get(str(vocab_id), "").strip()
            is_correct = user_answer.lower() == correct_word.lower()        
            results.append({
                "vocab_id": vocab_id,
                "word": correct_word,
                "users_answer": user_answer,
                "description": description,
                "correctness": is_correct
             })
   
        return results
    def update_training(self,training_id, success_rate:float):
        time_stamp = time.time()
        self._vocab_repository.update_training(training_id,success_rate,time_stamp)

    def get_vocab_count(self, user_id):
        return self._vocab_repository.count_users_vocabs(user_id)
    
    def get_users_trainings(self, user_id):
        return self._vocab_repository.get_users_trainings(user_id)
    

vocab_service = VocabService()