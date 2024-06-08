from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()
    print(Article.get_all_articles(get_db_connection()))


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
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    author = Author(name = author_name,conn= conn)


    # Create a magazine
    magazine = Magazine(name = magazine_name,category = magazine_category,conn = conn)
    
  

    # Create an article
    article = Article(title = article_title, content = article_content,author = author, magazine = magazine,conn = conn)

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    print(magazine.article_titles())

    conn.close()
    

"""    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["name"],author["id"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"])) """

if __name__ == "__main__":
    main()
