from models.author import Author

class Magazine:
    def __init__(self,name = "john doe", id = None,category = None,conn = None):
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
        if isinstance(name,str) and 2 <= len(name) <= 16:
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

    def articles(self):
        sql = "SELECT * FROM articles WHERE articles.magazine_id = ?"
        rows = self.cursor.execute(sql,(self.id,)).fetchall()
        return rows
    
    def contributors(self):
        sql = "SELECT * FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?"
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
        moreThanTwo = []
        contributors = self.contributors()
        for author in contributors:
            sql = "SELECT * FROM articles WHERE articles.author_id = ? and articles.magazine_id = ?"
            rows = self.cursor.execute(sql,(author[0],self.id))   
            if len(rows)>2:
                author_instance = Author(conn=self.conn,id = author[0],name = author[1])
                moreThanTwo.append(author_instance)
        return moreThanTwo



