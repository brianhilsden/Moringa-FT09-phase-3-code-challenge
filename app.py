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
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author,magazine,article
    author = Author(name=author_name,conn=conn)
    magazine = Magazine(name=magazine_name,category=magazine_category,conn=conn)
    article = Article(title=article_title,content=article_content,author=author,magazine=magazine,conn=conn)
    print(magazine.contributors())

    conn.close()
    
    
if __name__ == "__main__":
    main()
