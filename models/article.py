class Article:
    def __init__(self,id=None, title=None, content=None, author=None, magazine=None,conn = None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author.id
        self.magazine_id = magazine.id
        self.conn = conn

        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()

    def __repr__(self):
        return f'<Article {self.title}>'
    

    def add_to_database(self):
        sql = "INSERT INTO articles (title,content,author_id,magazine_id) VALUES (?,?,?,?)"
        self.cursor.execute(sql,(self.title,self.content,self.author_id,self.magazine_id))
        self.conn.commit()
        self.id = self.cursor.lastrowid

    @property
    def title(self):
        if not hasattr(self,"_title"):
            sql = "SELECT title FROM articles WHERE id = ?"
            row = self.cursor.execute(sql,(self.id,)).fetchone()
            if row:
                self._title = row[0]
        return self._title
        
    @title.setter
    def title(self,title):
        if isinstance(title,str) and 5 <= len(title) <= 50 and not hasattr(self,"_title") :
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters long and can only be set once.")

    def author(self):
        sql = "SELECT authors.name FROM articles INNER JOIN authors ON ? = authors.id"
        row = self.cursor.execute(sql,(self.author_id,)).fetchone()
        return row[0]
    
    def magazine(self):
        sql = "SELECT magazines.name FROM articles INNER JOIN magazines ON ? = magazines.id"
        row = self.cursor.execute(sql,(self.magazine_id,)).fetchone()
        return row[0]

    @classmethod
    def get_all_articles(cls,cursor):
        sql = "SELECT * FROM articles"
        articles = cursor.execute(sql).fetchall()
        return articles

