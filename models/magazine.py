from models.author import Author

class Magazine:
    def __init__(self,name = None, id = None,category = None,conn = None):
        self._id = id
        self._name = name
        self._category = category
        self.conn = conn
        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()


    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def add_to_database(self):
        sql_check = "SELECT id FROM magazines WHERE name = ? "
        result = self.cursor.execute(sql_check,(self.name,)).fetchone()
        if result:
            self.id = result[0]
        else:
            sql = "INSERT INTO magazines(name,category) VALUES (?,?)"
            self.cursor.execute(sql,(self.name,self.category))
            self.conn.commit()
            self.id = self.cursor.lastrowid

        

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,id):
        if isinstance(id,int):
            self._id = id
        else:
            raise TypeError("ID must be an integer")
    
    @property
    def name(self):
        if not hasattr(self,"_name"):
            sql = "SELECT name FROM magazines WHERE id = ?"
            row = self.cursor.execute(sql,(self.id,)).fetchone()
            if row:
                self._name = row[0]
        return self._name
    
    @name.setter
    def name(self,name):
        if not (isinstance(name, str) and 2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = name
        
    @property
    def category(self):
        if not hasattr(self,"_category"):
            sql = "SELECT category FROM magazines WHERE id = ?"
            row = self.cursor.execute(sql,(self.id,)).fetchone()
            if row:
                self._category=row[0]
        return self._category
            

    @category.setter
    def category(self,category):
        if isinstance(category,str) and len(category)>0:
            self._category = category
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        sql = "SELECT * FROM articles WHERE articles.magazine_id = ?"
        rows = self.cursor.execute(sql,(self.id,)).fetchall()
        return rows
    
    def contributors(self):
        sql = "SELECT authors.* FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?"
        rows = self.cursor.execute(sql,(self.id,)).fetchall()
        return rows


    @classmethod
    def get_all_magazines(cls,cursor):
        sql = "SELECT * FROM magazines"
        magazines = cursor.execute(sql).fetchall()
        return magazines
    
    def article_titles(self):
        articles = self.articles()
        return [item[1] for item in articles] if articles else None
    
    def contributing_authors(self):
        moreThanTwo = {}  # Use a dictionary to store unique authors
        contributors = self.contributors()
        for author in contributors:
            sql = "SELECT * FROM articles WHERE articles.author_id = ? and articles.magazine_id = ?"
            rows = self.cursor.execute(sql, (author[0], self.id)).fetchall()
            if len(rows) > 2:
                author_instance = Author(conn=self.conn, id=author[0], name=author[1])
                moreThanTwo[author_instance.id] = author_instance  # Store the author instance in the dictionary
        return list(moreThanTwo.values()) if moreThanTwo else None






