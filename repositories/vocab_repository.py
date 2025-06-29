import db

class VocabRepository:
    def vocab_exists(self, word:str )-> bool:
        sql = "Select id from vocabs where word = ?"
        return db.query(sql,[word])
    
    def save_vocabs(self, word: str, description: str, example: str, synonums: str, user_id:int,global_flag:int ):
        sql = "INSERT into vocabs (global_flag,word,w_description,example,synonyms,user_id) VALUES (?,?,?,?,?,?)"
        db.execute(sql,[global_flag,word,description,example,synonums,user_id ])
       
    def count_users_vocabs(self, user_id: int ): # To be replaced
        sql = """SELECT COUNT(*) FROM vocabs WHERE user_id = ?"""
        result = db.query(sql,[user_id])
        return result[0]
    ## Users statistics
    def get_users_vocab_stats(self, user_id):
        sql = """SELECT COUNT(id) as no_of_vocabs, SUM(global_flag) as total_global
                 FROM vocabs
                 WHERE user_id = ?"""
        result = db.query(sql,[user_id])[0]
        no_of_vocabs = result["no_of_vocabs"]
        no_of_global = result["total_global"]

        vocab_stats = {"no_of_vocabs":no_of_vocabs,
                       "no_of_global":no_of_global
                      }

        return vocab_stats
    def get_users_training_stats(self,user_id):
        #open training sessions
        sql = """SELECT COUNT(id) as count from training_sessions where user_id = ? """
        open_sessions = db.query(sql,[user_id])[0]["count"]
        #last executed training session
        sql2 = """SELECT success_rate FROM training_sessions WHERE user_id = ? ORDER BY last_accessed DESC LIMIT 1;"""
        last_row= db.query(sql2,[user_id])
        last_session_success = last_row[0]["success_rate"] if last_row else None
        sql3 = """SELECT COUNT(id) as count FROM vocab_status WHERE user_id = ? AND last_success_status = 8 """
        result = db.query(sql3,[user_id])
        current_known = result[0]["count"] or 0
        training_stats = {"open_sessions": open_sessions,
                          "last_session_success": last_session_success,
                          "current_known":current_known}
        return training_stats
    
    def get_users_suggestion_stats(self,user_id):
        sql = """SELECT count(id) as count FROM change_suggestions where creator_id = ?"""
        suggestions_created = db.query(sql,[user_id])[0]["count"] or 0
        sql2 = """SELECT count(id) as count FROM change_suggestions where creator_id = ? 
                  AND  change_status = 3 """
        own_suggestions_approved = db.query(sql2, [user_id])[0]["count"] or 0
        sql3 = """SELECT count(id) as count FROM change_suggestions where owner_id = ?"""
        suggestions_to_own = db.query(sql3,[user_id])[0]["count"] or 0
        suggestion_stats = {"suggestions_created": suggestions_created,
                            "own_suggestions_approved": own_suggestions_approved,
                            "suggestions_to_own": suggestions_to_own}
        return suggestion_stats
    ## Community statistics
    def get_community_vocab_stats(self):
        sql = """SELECT AVG(vocab_count) as average_vocabs FROM 
                (SELECT COUNT(id) as vocab_count FROM vocabs GROUP BY user_id)"""
        result = db.query(sql,[])
        average_vocabs = result[0]["average_vocabs"] or 0
        sql2 = """SELECT AVG(vocab_count) as average_vocabs_global FROM 
                (SELECT COUNT(id) as vocab_count FROM vocabs WHERE global_flag = 1 GROUP BY user_id)"""
        result2 = db.query(sql2,[])
        average_vocabs_global = result2[0]["average_vocabs_global"] or 0

        return{
        "avg_no_of_vocabs": average_vocabs,
        "avg_no_of_global": average_vocabs_global }

    def get_community_training_stats(self):
        sql = """SELECT AVG(training_count) as average_trainings FROM
                 (SELECT COUNT(id) as training_count from training_sessions GROUP BY user_id)"""
        result = db.query(sql,[])
        average_trainings = result[0]["average_trainings"] or 0

        sql2 = """WITH last_sessions AS (
             SELECT user_id, MAX(id) AS last_session
             FROM training_sessions
            GROUP BY user_id),per_user_stats AS (
            SELECT ls.user_id,
            SUM(CASE WHEN vs.last_success_status = 8 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS success_rate
            FROM training_items ti
            JOIN last_sessions ls ON ti.training_id = ls.last_session
            JOIN vocab_status vs ON vs.vocab_id = ti.vocab_id AND vs.user_id = ls.user_id
            GROUP BY ls.user_id)
            SELECT AVG(success_rate) AS avg_success_rate FROM per_user_stats"""
        result2 = db.query(sql2,[])
        last_session_average_correct = result2[0]["avg_success_rate"] or 0

        sql3 = """SELECT AVG(known_count) AS average_known FROM
                  (SELECT COUNT(id) as known_count FROM vocab_status WHERE
                   last_success_status = 8 GROUP BY user_id )"""
        result3 = db.query(sql3,[])
        average_known = result3[0]["average_known"] or 0

        return {
                "avg_open_sessions": average_trainings,
                "avg_last_session_success": last_session_average_correct,
                "avg_current_known": average_known
                }
    def get_community_suggestions_stats(self):
        sql = """SELECT AVG(suggestion_count) as average_suggestions FROM
                (SELECT COUNT(id) as suggestion_count FROM change_suggestions group by creator_id)"""
        result = db.query(sql,[])
        avg_suggestions_created = result[0]["average_suggestions"] or 0
        sql2 = """SELECT AVG(suggestions_approved) as avg_suggestions_approved FROM
                (SELECT COUNT(id) as suggestions_approved from change_suggestions WHERE change_status = 3
                GROUP BY creator_id)"""
        result2 = db.query(sql2,[])
        avg_suggestions_approved = result2[0]["avg_suggestions_approved"] or 0

        sql3 = """SELECT AVG(count_recieved) as avg_received FROM
                  (SELECT COUNT(id) as count_recieved FROM change_suggestions group by owner_id)"""
        result3 = db.query(sql3,[])
        avg_suggestions_received = result3[0]["avg_received"] or 0

        return {
            "avg_suggestions_created": avg_suggestions_created,
            "avg_own_suggestions_approved": avg_suggestions_approved,
            "avg_suggestions_to_own": avg_suggestions_received
            }

    ## Vocab selection
    def get_vocabs(self, user_id : int):
        sql = """SELECT a.id as id, a.word as word, a.w_description as w_description,
               a.example as example, a.synonyms as synonyms, a.user_id as user_id, 
               a.global_flag as global_flag, b.status_description as flag_description,
               d.status_description as last_test_status
               FROM vocabs as a LEFT JOIN status_categories as b ON a.global_flag = b.status_id 
               LEFT JOIN vocab_status as c ON c.vocab_id = a.id AND c.user_id = ?
               LEFT JOIN status_categories as d ON d.status_id = c.last_success_status
               WHERE a.user_id = ? 
               OR global_flag = 1
               GROUP BY a.id  
               ORDER BY CASE WHEN a.user_id = ? THEN 0 ELSE 1 END
               """
        result_set = db.query(sql,[user_id,user_id,user_id])
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
            return "Exception "+ str(id)
        return None
        

    def get_id(self, word:str)->int:
        sql = "SELECT id FROM vocabs where word = ?"
        result = db.query(sql,[word])
        return result
          
    def get_owner(self,id)->int:
        sql = "SELECT user_id FROM vocabs where id = ?"
        return db.query(sql,[id])
    
    def get_vocab(self,id):
        sql = """SELECT a.id as id, a.word as word, a.w_description as w_description,
        a.example as example, a.synonyms as synonyms, a.user_id as user_id, a.global_flag as global_flag, 
        b.status_description from vocabs as a
        LEFT JOIN  status_categories as b ON a.global_flag = b.status_id  where a.id = ?
        GROUP BY a.id """
        result = db.query(sql, [id])
        return result[0] if result else None
        
    def find_vocabs(self,search_string:str, user_id:int):
        sql = """SELECT a.id as id, a.word as word, a.w_description as w_description, a.example as example,
               a.synonyms as synonyms, a. user_id as user_id, a.global_flag as global_flag,
               b.status_description as flag_description 
               FROM vocabs as a LEFT JOIN status_categories as b ON a.global_flag = b.status_id 
               where (user_id = ? AND word like ?)
               OR (global_flag = 1  AND word like ?)
               GROUP by a.id
               ORDER BY CASE WHEN user_id = ? THEN 0 ELSE 1 END"""
        
        result = db.query(sql,[user_id,search_string,search_string, user_id])
        return result
        
    def get_vocabs_by_ids(self,user_id, ids):
        sql =  (
            "SELECT id, word, w_description, example, synonyms "
            "FROM vocabs "
            "WHERE (user_id = ? OR global_flag = 1) AND id IN ({})"
            "ORDER BY RANDOM()"
        ).format(",".join(["?"] * len(ids)))
        
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
    def update_training_description(self,training_id,session_description):
        sql = "UPDATE training_sessions set session_description = ? where id = ? "
        db.execute(sql,[session_description,training_id])
    def get_training_owner(self,training_id):
        sql = "SELECT user_id from training_sessions where id = ?"
        result = db.query(sql,[training_id])
        return result[0]

    def save_training(self,user_id,vocab_hash, time_stamp ,vocab_ids, session_description):
        sql1 = """INSERT INTO training_sessions (user_id,last_accessed, vocab_hash,
               success_rate, session_description) VALUES (?,?,?,?,?)"""
        db.execute(sql1,[user_id, time_stamp, vocab_hash,0.0,session_description])
        training_id = db.last_insert_id()
        
        sql2 = "INSERT into training_items (training_id,vocab_id) VALUES (?,?)"
        params = [(training_id, vocab_id) for vocab_id in vocab_ids]
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
        sql = """Select a.id AS id, PRINTF("%.1f%%",a.success_rate*100) AS success_rate,
          a.last_accessed AS last_accessed, a.session_description as session_description ,
          COUNT(b.id) AS no_of_vocabs FROM training_sessions AS a LEFT JOIN training_items AS b 
          ON a.id = b.training_id WHERE a.user_id = ?
          GROUP BY a.id, a.success_rate, a.last_accessed"""
        result = db.query(sql,[user_id])
        return result
    
    def update_training_vocabs(self, user_id, vocabs, status, timestamp):

        # Get the users vocabs with status
        sql1 = """SELECT vocab_id from vocab_status where user_id = ?"""
        existing_vocab_rows = db.query(sql1, [user_id])
        existing_vocab_ids = set(row["vocab_id"] for row in existing_vocab_rows)
        to_update = []
        to_insert = []
        for vocab_id in vocabs:
            if vocab_id in existing_vocab_ids:
                to_update.append([status, timestamp , user_id, vocab_id])
            else:
                to_insert.append([user_id, vocab_id , status , timestamp])
        if to_update:
            sql2 = """UPDATE vocab_status SET last_success_status = ?, last_updated = ?
                  WHERE user_id = ? AND vocab_id = ?"""
            db.execute_batch_insert(sql2,to_update)
        if to_insert:
            sql3 = """INSERT INTO vocab_status (user_id, vocab_id, last_success_status, last_updated)
                  VALUES (?, ?, ?, ?)"""
            db.execute_batch_insert(sql3,to_insert)

    def delete_training(self, training_id, user_id):
        sql1 = "DELETE FROM training_items where training_id = ?"
        db.execute(sql1,[training_id])
        sql2 = "DELETE FROM training_sessions where user_id = ? AND id = ?"
        db.execute(sql2,[user_id,training_id])


    def get_global_flag_values(self):
        sql = "SELECT status_id, status_description FROM status_categories WHERE category_type = ? "
        result = db.query(sql,["Visibility"])
        return result
    

    def get_total_no_of_vocabs(self):
        sql = "SELECT COUNT(id) as no_of_vocabs from vocabs"
        result = db.query(sql,[])
        return result
    
    ## Suggestions handling

    def save_vocab_suggestion(self, requester_id,owner_id,vocab_id, new_description, new_example, new_synonyms, comments,time_stamp ):
        sql = """INSERT into change_suggestions 
                (vocab_id,owner_id, creator_id, new_description, new_example, new_synonyms, change_status, comments, creation_time)
                values (?,?,?,?,?,?,?,?,?)"""
        db.execute(sql,[vocab_id,owner_id,requester_id,new_description,new_example,new_synonyms,2,comments,time_stamp])
        suggestion_id = db.last_insert_id
        return suggestion_id
  
    def get_suggestions_to_user(self, user_id):
        sql = """SELECT a.id as id, b.word as word,b.w_description as orig_description, b.example as orig_example,
                 b.synonyms as orig_synonyms, a.new_description as new_description, a.new_example as new_example,
                 a.new_synonyms as new_synonyms, a.comments as comments, a.creation_time as creation_time,
                 c.status_description as status from change_suggestions AS a
                 JOIN vocabs AS b ON a.vocab_id = b.id
                 JOIN status_categories AS c ON a.change_status = c.status_id
                 WHERE a.owner_id = ? AND a.change_status = 2
                 GROUP BY a.id
                 """
        result = db.query(sql,[user_id])
        return result
    def get_own_suggestions(self, user_id):
        sql = """SELECT a.id as id, b.word as word,b.w_description as orig_description, b.example as orig_example,
                 b.synonyms as orig_synonyms, a.new_description as new_description, a.new_example as new_example,
                 a.new_synonyms as new_synonyms, a.comments as comments, a.creation_time as creation_time,
                 c.status_description as status from change_suggestions AS a
                 JOIN vocabs AS b ON a.vocab_id = b.id
                 JOIN status_categories AS c ON a.change_status = c.status_id
                 WHERE a.creator_id = ? AND a.change_status = 2
                 GROUP BY a.id
                 """
        result = db.query(sql,[user_id])
        return result

    def get_suggestion(self,suggestion_id):
        sql = """SELECT id, vocab_id, owner_id,new_description, creator_id, new_example, new_synonyms, change_status
                 FROM change_suggestions where id = ?"""
        result = db.query(sql,[suggestion_id])
        return result

    def accept_suggestion(self,suggestion_id, vocab_id, new_description, new_example, new_synonyms):
        #Update vocab
        sql = """UPDATE vocabs SET  w_description = COALESCE(?,w_description), example = COALESCE(?,example),
                 synonyms =COALESCE(?,synonyms) WHERE id = ? 
                """
        db.execute(sql,[new_description,new_example,new_synonyms,vocab_id])
        # update suggestion
        self.set_suggestion_status(suggestion_id,3)

    def set_suggestion_status(self, suggestion_id, status):
        sql = "UPDATE change_suggestions SET change_status = ? WHERE id = ?"     
        db.execute(sql,[status,suggestion_id])   

vocab_repository = VocabRepository()