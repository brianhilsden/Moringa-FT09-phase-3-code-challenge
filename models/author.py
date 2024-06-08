class Author:
    def __init__(self,id=None, name=None, conn = None):
        self.name = name
        self.conn = conn
        self.id = id
      
        if conn:
            self.cursor = conn.cursor()
            self.add_author()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    def add_author(self):
        sql_check = "SELECT id FROM authors WHERE name = ? LIMIT 1"
        result = self.cursor.execute(sql_check,(self.name,)).fetchone()
        if result:
            self._id = result[0]
        else:
            sql = "INSERT INTO authors(name) VALUES (?)"
            self.cursor.execute(sql, (self.name,))
            self.conn.commit()
            self._id = self.cursor.lastrowid
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if isinstance(id,int):
            self._id = value

    @property
    def name(self): 
        if not hasattr(self,"_name"):
            sql = "SELECT name FROM author WHERE id = ?"
            self.cursor.execute(sql,(self.id,))
            row = self.cursor.fetchone()
            if row:
                self._name = row[0]
        return self._name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name) and not hasattr(self,"_name"):
            self._name = name
    
    def articles(self):
        sql = "SELECT * FROM authors INNER JOIN articles ON articles.author_id = ?"
        rows = self.cursor.execute(sql,(self.id,)).fetchall()
        return rows
    
    def magazines(self):
        sql = """SELECT * FROM magazines INNER JOIN articles ON articles.magazine_id = magazines.id WHERE articles.author_id = ?"""
        rows = self.cursor.execute(sql,(self.id,)).fetchall()
        return rows

    @classmethod
    def get_all_authors(cls,cursor):
        sql = "SELECT * FROM authors"
        authors = cursor.execute(sql).fetchall()
        return authors

