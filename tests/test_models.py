import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
import sqlite3

class TestModels(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        """)
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_author_init(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.name, "John Doe")
        self.assertIsNotNone(author.id)

    def test_author_add_author(self):
        author1 = Author(name="Jane Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        self.assertEqual(author1.id, author2.id)

    def test_author_id_property(self):
        author = Author(id=1,name="yobra", conn=self.conn)
        self.assertEqual(author.id, 1)
        with self.assertRaises(ValueError):
            author.id = "invalid"

    def test_author_name_property(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.name, "John Doe")
        with self.assertRaises(ValueError):
            author.name = 123

    def test_author_articles(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine, conn=self.conn)
        articles = author.articles()
        self.assertEqual(len(articles), 2)
        self.assertIn(article1.id, [article[0] for article in articles])
        self.assertIn(article2.id, [article[0] for article in articles])

    def test_author_magazines(self):
        author = Author(name="John Doe", conn=self.conn)
        magazine1 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        magazine2 = Magazine(name="Science Monthly", category="Science", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine1, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine2, conn=self.conn)
        magazines = author.magazines()
        self.assertEqual(len(magazines), 2)
        self.assertIn(magazine1.id, [magazine[0] for magazine in magazines])
        self.assertIn(magazine2.id, [magazine[0] for magazine in magazines])

    def test_author_get_all_authors(self):
        author1 = Author(name="John Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        all_authors = Author.get_all_authors(self.cursor)
        self.assertEqual(len(all_authors), 2)
        self.assertIn(author1.id, [author[0] for author in all_authors])
        self.assertIn(author2.id, [author[0] for author in all_authors])

    def test_magazine_init(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsNotNone(magazine.id)

    def test_magazine_add_to_database(self):
        magazine1 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        magazine2 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine1.id, magazine2.id)

    def test_magazine_id_property(self):
        magazine = Magazine(id=1,name="Today Daily",category="Sports", conn=self.conn)
        self.assertEqual(magazine.id, 1)
        with self.assertRaises(TypeError):
            magazine.id = "invalid"

    def test_magazine_name_property(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")
        with self.assertRaises(ValueError):
            magazine.name = "T"
        with self.assertRaises(ValueError):
            magazine.name = "TooLong"*5

    def test_magazine_category_property(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.category, "Technology")
        with self.assertRaises(ValueError):
            magazine.category = ""

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
        self.assertIn(author1.id, [author[0] for author in contributors])
        self.assertIn(author2.id, [author[0] for author in contributors])

    def test_magazine_get_all_magazines(self):
        magazine1 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        magazine2 = Magazine(name="Science Monthly", category="Science", conn=self.conn)
        all_magazines = Magazine.get_all_magazines(self.cursor)
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

    def test_magazine_contributing_authors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        author1 = Author(name="John Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author1, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author1, magazine=magazine, conn=self.conn)
        article3 = Article(title="Test Title 3", content="Test Content 3", author=author1, magazine=magazine, conn=self.conn)
        article4 = Article(title="Test Title 4", content="Test Content 4", author=author2, magazine=magazine, conn=self.conn)
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
        self.assertIn(author1, contributing_authors)

    def test_article_creation(self):
        self.author = Author(name="John Doe", conn=self.conn)
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title,"Test Title")
        self.assertEqual(article.content,"Test Content")
        self.assertEqual(article.author_id,self.author.id)
        self.assertEqual(article.magazine_id,self.magazine.id)

    def test_article_title_setter_invalid_title(self):
        self.author = Author(name="John Doe", conn=self.conn)
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Initial Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)  # Initialize with a title
        with self.assertRaises(ValueError):
            article.title = "Inv"  # Too short
        with self.assertRaises(ValueError):
            article.title = "Too Long Title" * 10  # Too long
        with self.assertRaises(ValueError):
            article.title = 123  # Not a string
        with self.assertRaises(ValueError):
            article.title = "Already Set"  # Cannot set title twice

    def test_article_author(self):
        self.author = Author(name="John Doe", conn=self.conn)
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)
        self.assertEqual(article.author(), self.author.name)

    def test_article_magazine(self):
        self.author = Author(name="John Doe", conn=self.conn)    
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)
        self.assertEqual(article.magazine(), self.magazine.name)




if __name__ == "__main__":
    unittest.main()