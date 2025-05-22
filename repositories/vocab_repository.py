import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[0,word,description,example,synonums,user_id ])
       

    def get_vocabs(self, user_id : int):
        sql = """SELECT id, word, w_description, example, synonyms, user_id from vocabs where user_id = ? 
               OR global_flag = 1  
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        result_set = db.query(sql,[user_id,user_id])
        return result_set 
    def edit_vocab(self,vocab):
        sql = """UPDATE vocabs set word = ?w_description = ? example = ?
                 synonums = ? global_flag = ? word = ? WHERE id = ? 
                """
        db.execute(sql,[vocab.word,vocab.w_description,vocab.example,vocab.synonums,vocab.global_flag,vocab.id])
        
    def del_vocab(self,id:int):
        sql = "DELETE from vocabs where id = ?"
        db.execute(sql,id)
        
    def get_id(self, word:str)->int:
        sql = "SELECT id FROM vocabs where word = ?"
        return db.query(sql,id)       
    def get_owner(self,id)->int:
        sql = "SELECT user_id FROM vocabs where id = ?"
        return db.query(sql,id)
    
    def get_vocab(self,id):
        sql = "SELECT word, w_description, example, synonyms, user_id, global_flag from vocabs where id = ? "
        return db.query(sql, id)
        
    
        
vocab_repository = VocabRepository()