import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[0,word,description,example,synonums,user_id ])
       

    def get_vocabs(self, user_id : int):
        sql = """SELECT id, word, w_description, example, synonyms, user_id, global_flag from vocabs where user_id = ? 
               OR global_flag = 1  
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        result_set = db.query(sql,[user_id,user_id])
        return result_set 
    def edit_vocab(self,word:str, description:str, example:str, synonyms:str, global_flag:int, id:int):
        sql = """UPDATE vocabs set word = ?, w_description = ?, example = ?,
                 synonyms = ?, global_flag = ? WHERE id = ? 
                """
        db.execute(sql,[word,description,example,synonyms,global_flag,id])
        
    def del_vocab(self,id:int):
        sql = "delete from vocabs where id = ?"
        try:
            db.execute(sql,[id])
        except Exception:
            return "Exception"
        return None
        

    def get_id(self, word:str)->int:
        sql = "SELECT id FROM vocabs where word = ?"
        result = db.query(sql,[word]) 
        return result
          
    def get_owner(self,id)->int:
        sql = "SELECT user_id FROM vocabs where id = ?"
        return db.query(sql,[id])
    
    def get_vocab(self,id):
        sql = "SELECT id, word, w_description, example, synonyms, user_id, global_flag from vocabs where id = ? "
        result = db.query(sql, [id])
        return result[0] if result else None
        
    def find_vocabs(self,search_string:str, user_id:int):
        sql = """SELECT id, word, w_description, example, synonyms, user_id, global_flag from vocabs 
               where (user_id = ? AND word like ?)
               OR (global_flag = 1  AND word like ?)
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        like = "%" + search_string + "%"
        result = db.query(sql,[user_id,like,like, user_id])
        return result      
        
    def get_vocabs_by_ids(self,user_id, ids):
        sql =  (
            "SELECT id, word, w_description, example "
            "FROM vocabs "
            "WHERE (user_id = ? OR global_flag = 1) AND id IN ({})"
            "ORDER BY RANDOM()"
        ).format(','.join(['?'] * len(ids)))
        
        params = [user_id]+ids
        result = db.query(sql,params)
        return result
    def save_training(self,user_id,vocab_hash, time_stamp ,vocab_ids):
        sql1 = "INSERT INTO training_sessions (user_id,last_accessed, vocab_hash, success_rate) VALUES (?,?,?,?)"
        db.execute(sql1,[user_id, time_stamp, vocab_hash,0.0])  
        training_id = db.last_insert_id()

        sql2 = "INSERT into raining_items (training_id,vocab_id,succes_rate) VALUES (?,?,?)"
        params = [(training_id, vocab_id, 0) for vocab_id in vocab_ids]
        db.execute_batch_insert(sql2,params)

vocab_repository = VocabRepository()