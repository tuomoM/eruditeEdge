import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[1,word,description,example,synonums,user_id ])
       

    def get_vocabs(self, user_id : int):
        sql = """SELECT word, w_description, example, synonyms from vocabs where user_id = ? 
               OR global_flag = 1  
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        result_set = db.query(sql,[user_id,user_id])
        return result_set 

vocab_repository = VocabRepository()