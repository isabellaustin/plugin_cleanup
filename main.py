import json
from wordpress import wp
import colorama
import mysql.connector
import logging
from phpserialize import *

def main(blogs) -> None:
    """creates a dict of blogs in the database"""
    user_blogs = {}
    blogs.get_user_blogs(user_blogs, cnx)
    
    logger.setLevel(logging.INFO)

    for site in user_blogs.items():
        site_id = site[0]
        site_path = site[1]

        blogs.activate_plugin('a:1:{i:0;s:33:"classic-editor/classic-editor.php";}', site_path, site_id,logger,cnx)

    cnx.close()

if __name__ == "__main__":
    colorama.init(autoreset=True)

    with open('config.json', 'r') as f:
        cfg=json.load(f)
        exclude_users = cfg["exclude_users"]
        exclude_outside_users = cfg["exclude_outside_users"]

    cnx = mysql.connector.connect(user=cfg["db_username"], password=cfg["db_password"], host="docker-dev.butler.edu", database="wp_blogs_dev")

    blogs = wp(url = cfg["url"],
                username = cfg["username"],
                password = cfg["password"])
    
    log_file = cfg['log_file']

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh = logging.FileHandler(log_file, mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    main(blogs)