from models.article import Article
from models.author import Author
from models.magazine import Magazine
from database.connection import get_db_connection
 

conn = get_db_connection()

def exit_program():
    print("Goodbye")
    exit()

def add_entry():
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    try:
        author = Author(name=author_name,conn=conn)
        magazine = Magazine(name=magazine_name,category=magazine_category,conn=conn)
        article = Article(title=article_title,content=article_content,author=author,magazine=magazine,conn=conn)
        print("Entry added successfully")
    except Exception as e:
        print("Error creating entry: ",e)
        

def author_articles():
    author_name = input("Enter author's name: ")
    author = Author.find_by_name(conn,author_name)
    if author:
        print(f"Author articles are: {author.articles()}")
    else:
        print("Author does not exist")

def author_magazines():
    author_name = input("Enter author's name: ")
    author = Author.find_by_name(conn,author_name)
    if author:
        print(f"Author magazines are: {author.magazines()}")
    else:
        print("Author does not exist")

def all_authors():
    authors = Author.get_all_authors(conn)
    print(f"Authors are {authors}")

def magazine_articles():
    magazine_name = input("Enter the magazine's name: ")
    magazine = Magazine.find_by_name(conn,magazine_name)
    if magazine:
        print(f"Magazine articles are: {magazine.articles()}")
    else:
        print("Magazine does not exist")

def magazine_contributors():
    magazine_name = input("Enter the magazine's name: ")
    magazine = Magazine.find_by_name(conn,magazine_name)
    if magazine:
        print(f"Magazine contributors are: {magazine.contributors()}")
    else:
        print("Magazine does not exist")

def article_titles():
    magazine_name = input("Enter the magazine's name: ")
    magazine = Magazine.find_by_name(conn,magazine_name)
    if magazine:
        print(f"Magazine article titles are: {magazine.article_titles()}")
    else:
        print("Magazine does not exist")

def contributing_authors():
    magazine_name = input("Enter the magazine's name: ")
    magazine = Magazine.find_by_name(conn,magazine_name)
    if magazine:
        print(f"Magazine contributing authors are: {magazine.contributing_authors()}")
    else:
        print("Magazine does not exist")

def all_magazines():
    magazines = Magazine.get_all_magazines(conn)
    print(f"All magazines in db are: {magazines}")

def author():
    article_id = int(input("Enter the article's id: "))
    article = Article.find_by_id(conn,article_id)
    if article:
        print(f"The author of the article is: {article.author()}")
    else:
        print("Article does not exist")

def magazine():
    article_id = int(input("Enter the article's id: "))
    article = Article.find_by_id(conn,article_id)
    if article:
        print(f"The magazine of the article is: {article.magazine()}")
    else:
        print("Article does not exist")

def all_articles():
    articles = Article.get_all_articles(conn)
    if articles:
        print(f"All the articles in the database are: {articles}")
    else:
        print("Article does not exist")





