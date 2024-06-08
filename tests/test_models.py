import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
import sqlite3

class TestModels(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''')
        self.cursor.execute('''CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )''')
        self.cursor.execute('''CREATE TABLE magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT
        )''')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    # ... (Your existing tests for Author, Article, and Magazine) ...

    def test_author_creation(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.name, "John Doe")

    def test_author_name_attribute(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertTrue(hasattr(author, 'name'))

    def test_author_name_type(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertTrue(isinstance(author.name, str))

    def test_author_id_attribute(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertTrue(hasattr(author, 'id'))

    def test_author_id_type(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertTrue(isinstance(author.id, int))

    def test_author_add_author(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.id, 1)
        self.cursor.execute("SELECT * FROM authors WHERE name = 'John Doe'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "John Doe")

    def test_author_add_author_existing(self):
        author1 = Author(name="Jane Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        self.assertEqual(author1.id, 1)
        self.assertEqual(author2.id, 1)


    def test_author_magazines(self):
        author = Author(name="John Doe", conn=self.conn)
        self.cursor.execute("INSERT INTO magazines(name, category) VALUES ('Tech Weekly', 'Technology')")
        self.conn.commit()
        self.cursor.execute("INSERT INTO articles(title, content, author_id, magazine_id) VALUES ('Test Title', 'Test Content', 1, 1)")
        self.conn.commit()
        magazines = author.magazines()
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0][1], "Tech Weekly")

    def test_author_get_all_authors(self):
        author = Author(name="John Doe", conn=self.conn)
        self.cursor.execute("INSERT INTO authors(name) VALUES ('Jane Doe')")
        self.conn.commit()
        all_authors = Author.get_all_authors(self.cursor)  # Call the class method
        self.assertEqual(len(all_authors), 2)
        self.assertIn(author.id, [author[0] for author in all_authors])  # Check for IDs in the result
        self.assertIn(1, [author[0] for author in all_authors])  # Check for ID of 'Jane Doe'


    def test_article_creation(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine, conn=self.conn)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.author_id, author.id)
        self.assertEqual(article.magazine_id, magazine.id)

    def test_article_add_to_database(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine, conn=self.conn)
        self.assertIsNotNone(article.id)
        self.cursor.execute("SELECT * FROM articles WHERE title = 'Test Title'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Test Title")
        self.assertEqual(result[2], "Test Content")
        self.assertEqual(result[3], author.id)
        self.assertEqual(result[4], magazine.id)

    def test_article_title_getter(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine, conn=self.conn)
        self.assertEqual(article.title, "Test Title")


    def test_article_author(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine, conn=self.conn)
        self.assertEqual(article.author(), "John Doe")

    def test_article_magazine(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine, conn=self.conn)
        self.assertEqual(article.magazine(), "Tech Weekly")

    def test_article_get_all_articles(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine, conn=self.conn)
        all_articles = Article.get_all_articles(self.cursor)  # Call the class method
        self.assertEqual(len(all_articles), 2)
        self.assertIn(article1.id, [article[0] for article in all_articles])  # Check for IDs in the result
        self.assertIn(article2.id, [article[0] for article in all_articles])

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_magazine_add_to_database(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertIsNotNone(magazine.id)
        self.cursor.execute("SELECT * FROM magazines WHERE name = 'Tech Weekly'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Tech Weekly")
        self.assertEqual(result[2], "Technology")

    def test_magazine_name_getter(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_magazine_name_setter(self):
        magazine = Magazine(category="Technology", conn=self.conn)
        magazine.name = "New Tech Weekly"
        self.assertEqual(magazine.name, "New Tech Weekly")

 
    def test_magazine_category_getter(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.category, "Technology")

    def test_magazine_category_setter(self):
        magazine = Magazine(name="Tech Weekly", conn=self.conn)
        magazine.category = "Science"
        self.assertEqual(magazine.category, "Science")

    def test_magazine_articles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        author = Author(name="John Doe", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine, conn=self.conn)
        articles = magazine.articles()
        self.assertEqual(len(articles), 2)
        self.assertIn(article1.id, [article[0] for article in articles])
        self.assertIn(article2.id, [article[0] for article in articles])

    def test_magazine_contributors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        author1 = Author(name="John Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author1, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author2, magazine=magazine, conn=self.conn)
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 2)
        self.assertIn(author1.id, [contributor[0] for contributor in contributors])
        self.assertIn(author2.id, [contributor[0] for contributor in contributors])

    def test_magazine_get_all_magazines(self):
        magazine1 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        magazine2 = Magazine(name="Science Monthly", category="Science", conn=self.conn)
        all_magazines = Magazine.get_all_magazines(self.cursor)  # Call the class method
        self.assertEqual(len(all_magazines), 2)
        self.assertIn(magazine1.id, [magazine[0] for magazine in all_magazines])
        self.assertIn(magazine2.id, [magazine[0] for magazine in all_magazines])


    def test_magazine_article_titles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        author = Author(name="John Doe", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine, conn=self.conn)
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 2)
        self.assertIn("Test Title 1", titles)
        self.assertIn("Test Title 2", titles)



if __name__ == "__main__":
    unittest.main()