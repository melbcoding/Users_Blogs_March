from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post_model


class User:
    my_db="blog_schema"
    def __init__(self, data):
        self.id = data['id']
        self.f_name=data['first_name']
        self.l_name=data['last_name']
        self.email=data['email']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.all_posts = []

    # queries with CRUD and OOP

    @classmethod
    def get_all(cls):
        query='''
            SELECT * FROM users;
        '''
        results= connectToMySQL(cls.my_db).query_db(query)

        print(results)

        user_objects=[]
        for record in results:
            one_user= cls(record)
            user_objects.append(one_user)
            
        return user_objects
    

    @classmethod
    def save_user(cls, form_data):
        query= '''
                INSERT INTO users
                (first_name, last_name, email)
                VALUES
                (%(f_name)s, %(l_name)s, %(email)s);
        '''
        results= connectToMySQL(cls.my_db).query_db(query, form_data)

        return results
    
    @classmethod
    def get_user_with_posts(cls):
        query= '''
            SELECT * FROM users
            LEFT JOIN posts
            ON users.id = posts.user_id
            WHERE users.id = 1
        '''
        results= connectToMySQL(cls.my_db).query_db(query)
        print(results)
        one_user = cls(results[0])
        for row in results:
            post_data={
                "id" : row['posts.id'], 
                "user_id": row['user_id'],
                "title":row['title'],
                "content": row['content'],
                "created_at": row['posts.created_at'],
                "updated_at": row['posts.updated_at']
            }
            one_user.all_posts.append(post_model.Post(post_data))
        return one_user



            

