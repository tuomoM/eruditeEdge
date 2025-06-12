import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[0,word,description,example,synonums,user_id ])
       
    def count_users_vocabs(self, user_id: int ): # To be replaced
        sql = """SELECT COUNT(*) FROM vocabs WHERE user_id = ?"""
        result = db.query(sql,[user_id])
        return result[0]
    
    def get_users_vocab_stats(self, user_id):
        sql = """SELECT COUNT(id) as no_of_vocabs, SUM(global_flag) as total_global
                 FROM vocabs
                 WHERE user_id = ?"""
        result = db.query(sql,[user_id])
        return result[0]
    
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
    
    def get_training_id(self,user_id,vocab_hash):
        sql = """SELECT id FROM training_sessions WHERE user_id = ? AND vocab_hash = ?"""
        result = db.query(sql,[user_id,vocab_hash])
        if result:
            id = result[0][0]
            return id
        else:
            return None

    def get_training_owner(self,training_id):
        sql = "SELECT user_id from training_sessions where id = ?"
        result = db.query(sql,[training_id])
        return result[0]

    def save_training(self,user_id,vocab_hash, time_stamp ,vocab_ids):
        sql1 = "INSERT INTO training_sessions (user_id,last_accessed, vocab_hash, success_rate) VALUES (?,?,?,?)"
        db.execute(sql1,[user_id, time_stamp, vocab_hash,0.0])  
        training_id = db.last_insert_id()
        
        sql2 = "INSERT into training_items (training_id,vocab_id,success_rate) VALUES (?,?,?)"
        params = [(training_id, vocab_id, 0) for vocab_id in vocab_ids]
        db.execute_batch_insert(sql2,params)
        return training_id
    
    def get_answers(self,training_id):
        sql = """SELECT b.id, b.word, b.w_description 
                 FROM training_items AS a 
                 JOIN vocabs AS b ON a.vocab_id = b.id 
                 WHERE a.training_id = ?"""
        result = db.query(sql,[training_id])
        return result
    

    def update_training(self,training_id, success_rate, time_stamp):
        sql = """UPDATE training_sessions set success_rate = ?, last_accessed = ? WHERE id = ?"""
        db.execute(sql,[success_rate,time_stamp, training_id])
       
    def get_users_trainings(self, user_id):
        sql = """Select a.id AS id, PRINTF("%.1f%%",a.success_rate*100) AS success_rate, a.last_accessed AS last_accessed,
          COUNT(b.id) AS no_of_vocabs FROM training_sessions AS a LEFT JOIN training_items AS b 
          ON a.id = b.training_id WHERE a.user_id = ?
          GROUP BY a.id, a.success_rate, a.last_accessed"""
        result = db.query(sql,[user_id])
        return result
    def delete_training(self, training_id, user_id):
        sql1 = "DELETE FROM training_items where training_id = ?"
        db.execute(sql1,[training_id])
        sql2 = "DELETE FROM training_sessions where user_id = ? AND id = ?"
        db.execute(sql2,[user_id,training_id])
vocab_repository = VocabRepository()