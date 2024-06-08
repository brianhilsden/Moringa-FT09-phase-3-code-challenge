from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    '''
        Articles methods available:
            - author()                  Returns author of the article  (python class object)
            - magazine()                Returns magazine in which the article is contained  (python class object)
            - get_all_articles(conn)    Takes conn as argument, returns list of all the articles  (python class objects)


        Magazine methods available:
            - articles()                Returns list of all articles in the magazine  (python class objects)
            - contributors()            Returns list of all authors who have written articles in the magazine  (python class objects)
            - article_titles()          Returns string titles of the articles in the magazine  (strings)
            - contributing_authors()    Returns list of all authors who have written more than two articles in the magazine (python class objects)
            - get_all_magazines(conn)   Takes conn as argument, returns list of all the magazines  (python class objects)


        Author methods available:
            - articles()                Returns list of all articles the author has written  (python class objects)
            - magazines()               Returns list of all magazines the author has contributed to  (python class objects)
            - get_all_authors(conn)     Takes conna as argument, returns list of all authors  (python class objects)
    '''


    # Create an author,magazine,article
    author = Author(name=author_name,conn=conn)
    magazine = Magazine(name=magazine_name,category=magazine_category,conn=conn)
    article = Article(title=article_title,content=article_content,author=author,magazine=magazine,conn=conn)
    
    magazines = Magazine.get_all_magazines(conn)
    authors = Author.get_all_authors(conn)
    articles = Article.get_all_articles(conn)

    conn.close()

    # Display results for all magazines,authors,articles
    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)

    print("\nAuthors:")
    for author in authors:
        print(author)

    print("\nArticles:")
    for article in articles:
        print(article)
    
    
if __name__ == "__main__":
    main()
