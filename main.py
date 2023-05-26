import json
from wordpress import wp
import colorama
import mysql.connector

def main(blogs) -> None:
    """creates a list of blogs in the database"""
    user_blogs = {}
    blogs.get_user_blogs(user_blogs, cnx)
    sites = user_blogs.values()
    
    for site in sites:
        blogs.activate_plugin("classic-editor", site)

    cnx.close()

if __name__ == "__main__":
    colorama.init(autoreset=True)
    cnx = mysql.connector.connect(user="wordpress", password="4AbyJVrcPTH6aHgfAqt3", host="mysql-1.butler.edu", database="wp_blogs_dev")

    with open('config.json', 'r') as f:
        cfg=json.load(f)
        exclude_users = cfg["exclude_users"]
        exclude_outside_users = cfg["exclude_outside_users"]

    blogs = wp(url = cfg["url"],
                username = cfg["username"],
                password = cfg["password"])

    main(blogs)