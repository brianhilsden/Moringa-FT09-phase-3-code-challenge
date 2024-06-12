from database.setup import create_tables

from helpers import (
    exit_program,
    add_entry,
    author_articles,
    author_magazines,
    all_authors,
    magazine_articles,
    magazine_contributors,
    article_titles,
    contributing_authors,
    all_magazines,
    author,
    magazine,
    all_articles

)

def main():
    create_tables()
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            inner_menu(add_entry)
        elif choice == "2":
            inner_menu(author_articles)
        elif choice == "3":
            inner_menu(author_magazines)
        elif choice == "4":
            inner_menu(all_authors)
        elif choice == "5":
            inner_menu(magazine_articles)
        elif choice == "6":
            inner_menu(magazine_contributors)
        elif choice == "7":
            inner_menu(article_titles)
        elif choice == "8":
            inner_menu(contributing_authors)
        elif choice == "9":
            inner_menu(all_magazines)
        elif choice == "10":
            inner_menu(author)
        elif choice == "11":
            inner_menu(magazine)
        elif choice == "12":
            inner_menu(all_articles)
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add new entry")
    print("2. List specific author's articles")
    print("3. List specific author's magazines")
    print("4: List all authors")
    print("5: List specific magazine's articles")
    print("6: List specific magazine's contributors")
    print("7. List specific magazine's article titles")
    print("8. List specific magazine's contributing authors")
    print("9. List all magazines")
    print("10: Get author of specific article")
    print("11: Get magazine of specific article")
    print("12: List all articles")

def inner_menu(action):
    while True:
        action()
        print("\nEnter 't' to try again, 'b' to go back to main menu or 'q' to quit.")
        choice = input("> ")
        if choice == "b":
            break
        elif choice == "q":
            exit_program()
        elif choice == "t":
            pass
        else:
            print("Invalid entry")

    

if __name__ == "__main__":
    main()