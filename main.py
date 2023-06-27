import json
from wordpress import wp
import colorama
import mysql.connector
from tqdm import tqdm
import logging

def main(blogs) -> None:
    """creates a list of blogs in the database"""
    user_blogs = {}
    blogs.get_user_blogs(user_blogs, cnx)
    sites = user_blogs.values()
    site_paths = list(user_blogs.values())
    site_ids = list(user_blogs.keys())
    
    logger.setLevel(logging.INFO)

    # plugin = ""
    # for site in sites:
        # index = site_paths.index(f"{site}")
        # site_id = site_ids[index]

        # # for slug in plugin_slug:

        # plugin_status = blogs.activate_plugin(plugin, site, site_id,cnx)
        # logger.info(f"{site}: {plugin_status}")
        
    plugin_status = blogs.activate_plugin('a:1:{i:0;s:33:"classic-editor/classic-editor.php";}', '/', 1,cnx)
    print(plugin_status)
    #what are we activating based on? blog_id and then getting serialised plugin string? or just getting the serialised plugin string initially

    cnx.close()

if __name__ == "__main__":
    colorama.init(autoreset=True)
    cnx = mysql.connector.connect(user="wordpress", password="4AbyJVrcPTH6aHgfAqt3", host="docker-dev.butler.edu", database="wp_blogs_dev")

    with open('config.json', 'r') as f:
        cfg=json.load(f)
        exclude_users = cfg["exclude_users"]
        exclude_outside_users = cfg["exclude_outside_users"]

    blogs = wp(url = cfg["url"],
                username = cfg["username"],
                password = cfg["password"])
    
    log_file = cfg['log_file']

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_file, mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    main(blogs)