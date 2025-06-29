from repositories.vocab_repository import VocabRepository
from repositories.vocab_repository import vocab_repository as default_vocab_repository
import hashlib
from datetime import datetime


class VocabService:
    def __init__(self,vocab_repository:VocabRepository = default_vocab_repository )-> None:
        self._vocab_repository = vocab_repository

    def add_vocab(self, word: str,description: str, example: str, synonums: str, user_id:int, global_flag:int):
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
        self._vocab_repository.save_vocabs(word.capitalize(),description,example,synonums,user_id,global_flag)

    def get_vocabs(self,user_id):
        return self._vocab_repository.get_vocabs(user_id)
    
    
    def edit_vocab(self, vocab ,word:str, description:str, example:str, synonyms:str, global_flag: int ):
        id = vocab["id"]
        if not all([word,description,example,synonyms]):
            return "No field can be left empty"
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

        if "*" in search_string:
            search_string = search_string.replace("*","%")
        else:
            search_string = f"%{search_string}%"

        return self._vocab_repository.find_vocabs(search_string,user_id)
    
  
    def get_vocabset(self,user_id:int, ids):
        return self._vocab_repository.get_vocabs_by_ids(user_id, ids)
        
    def generate_hash(self,vocab_ids):
        vocab_ids_copy = vocab_ids[:]
        vocab_ids_copy.sort()
        vocab_ids_str = ','.join(map(str, vocab_ids_copy))
        hash_value = hashlib.sha256(vocab_ids_str.encode()).hexdigest()
        return hash_value
    
    def get_training_id(self,user_id, vocab_ids,session_description):
        vocab_hash = self.generate_hash(vocab_ids)
        id = self._vocab_repository.get_training_id(user_id,vocab_hash)
        if id is None:
            result = self.save_training(user_id,vocab_ids, vocab_hash, session_description)
            return result
        else:
            self._vocab_repository.update_training_description(id,session_description)
            return id

    def save_training(self, user_id, vocab_ids, vocab_hash,session_description):
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        training_id = self._vocab_repository.save_training(user_id,vocab_hash,time_stamp,vocab_ids, session_description)
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
    #def update_vocab_success(self,user_id,vocab_ids, training_id):

    def update_training(self,training_id, success_rate:float):
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        self._vocab_repository.update_training(training_id,success_rate,time_stamp)
    def update_training_vocabs(self, answers, user_id):
        succes_vocabs = []
        failed_vocabs = []
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        for answer in answers:
            if answer["correctness"]:
                succes_vocabs.append(int(answer["vocab_id"]))
            else:
                failed_vocabs.append(int(answer["vocab_id"]))
        if succes_vocabs:
            self._vocab_repository.update_training_vocabs(user_id,succes_vocabs,8,time_stamp) 
        if failed_vocabs:
            self._vocab_repository.update_training_vocabs(user_id,failed_vocabs,7,time_stamp) 
            
    def get_vocab_count(self, user_id):
        return self._vocab_repository.count_users_vocabs(user_id)
    def get_users_vocab_stats(self, user_id):
        return self._vocab_repository.get_users_vocab_stats(user_id)


    def get_users_trainings(self, user_id):
        result= self._vocab_repository.get_users_trainings(user_id)
        
        return result
    def delete_training(self,training_id, user_id ):
        owner = self._vocab_repository.get_training_owner(training_id)[0]
        if user_id is not owner:
            return "Error: Not possible to delete other users sessions"
        self._vocab_repository.delete_training(training_id,user_id)

    def get_training_set(self,training_id, user_id):
        owner = self._vocab_repository.get_training_owner(training_id)[0]
        if user_id is not owner:
            return "Error: Not possible to test other users sessions"
        vocabs = self._vocab_repository.get_answers(training_id)
        return vocabs
    def get_vocab_categories(self):
        return self._vocab_repository.get_global_flag_values()
    
    def get_total_no_of_vocabs(self):
        return self._vocab_repository.get_total_no_of_vocabs()
  
    def create_change_suggestion(self,vocab_id,user_id, new_description, new_example,new_synonyms,comments):
        if not any({new_description,new_example,new_synonyms}):
            return "Request atleast one change to submit change suggestion"
        
        vocab = self._vocab_repository.get_vocab(vocab_id)

        if new_description and vocab["word"] in new_description:
            return "Do not include the word in the description"
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._vocab_repository.save_vocab_suggestion(user_id,vocab["user_id"],vocab_id,new_description,new_example,new_synonyms, comments,time_stamp)
        return None
    
    def get_suggestions_to(self,user_id):
        return self._vocab_repository.get_suggestions_to_user(user_id)
    def get_own_suggestions(self,user_id):
        return self._vocab_repository.get_own_suggestions(user_id)
    
    def accept_suggestion(self, suggestion_id, user_id):
        suggestion = self._vocab_repository.get_suggestion(suggestion_id)[0]
        if not suggestion:
            return "Error suggestion not found"
        if suggestion["owner_id"] != user_id:
            return "Error not authorized to accept this suggestion"
        if suggestion["change_status"] != 2:
            return "Error Suggestion not possible to approve"

        if suggestion["new_description"] != "":
            new_description = suggestion["new_description"]
        else:
            new_description = None
        if suggestion["new_example"] != "":
            new_example = suggestion["new_example"]
        else:
            new_example = None
        if suggestion["new_synonyms"] != "":
            new_synonyms = suggestion["new_synonyms"]
        else:
            new_synonyms = None                     
        self._vocab_repository.accept_suggestion(suggestion_id,suggestion["vocab_id"],new_description,new_example,new_synonyms)

    def reject_suggestion(self,suggestion_id,user_id):
        suggestion = self._vocab_repository.get_suggestion(suggestion_id)[0]
        if not suggestion:
            return "Error suggestion not found"
        if suggestion["owner_id"] != user_id:
            return "Error not authorized to reject this suggestion"
        if suggestion["change_status"] != 2:
            return "Error Suggestion not possible to reject"
        self._vocab_repository.set_suggestion_status(suggestion_id,4)
    def cancel_suggestion(self,suggestion_id,user_id):
        suggestion = self._vocab_repository.get_suggestion(suggestion_id)[0]
        if not suggestion:
            return "Error suggestion not found"
        if suggestion["creator_id"] != user_id:
            return "Error not authorized to cancel this suggestion"
        if suggestion["change_status"] != 2:
            return "Error Suggestion not possible to cancel"
        self._vocab_repository.set_suggestion_status(suggestion_id,4)
vocab_service = VocabService()
