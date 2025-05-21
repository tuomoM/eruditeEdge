import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[0,word,description,example,synonums,user_id ])
       

    def get_vocabs(self, user_id : int):
        sql = """SELECT word, w_description, example, synonyms, user_id from vocabs where user_id = ? 
               OR global_flag = 1  
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        result_set = db.query(sql,[user_id,user_id])
        return result_set 
    def edit_vocab(self,word:str, description: str, example: str, synonums: str, user_id: int):
        return 0
    def del_vocab(self,word:str) -> bool:
        return False

        
vocab_repository = VocabRepository()