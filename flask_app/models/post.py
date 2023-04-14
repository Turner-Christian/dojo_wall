from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
import re

class Post:
    DB = 'dojo_wall_schema'
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']

    @classmethod
    def create_post(cls,data):
        query = """
        INSERT INTO post(content,user_id)
        VALUES(%(content)s, %(user_id)s)
        """
        return MySQLConnection(cls.DB).query_db(query,data)

    @classmethod
    def show_all_posts(cls):
        query = """
        select * from post
        join users on post.user_id = users.id
        order by post.created_at desc;
        """
        result = MySQLConnection(cls.DB).query_db(query)
        all_posts = []
        for row in result:
            posting_user = User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_post = Post({
                'id': row['id'],
                'content': row['content'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
            all_posts.append(new_post)
        return all_posts

    @classmethod
    def delete_post(cls,data):
        query = 'DELETE FROM post WHERE id = %(id)s'
        return MySQLConnection(cls.DB).query_db(query,data)

