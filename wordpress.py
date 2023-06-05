from typing import List
import base64
from colorama import Fore, Back
import subprocess

class wp:
    def __init__(self, url: str = "https://localhost", username: str = "", password: str = "") -> None:
        self.url = url
        self.api_url = f"{self.url}/wp-json/wp/v2/"
        self.username = username
        self.password = password
        self.make_cred()
        self.headers = {'Authorization': f'Basic {self.token}'}


    def __str__(self) -> str:
        return f"<wp({self.url})>"


    def make_cred(self) -> None:
        credentials = self.username + ":" + self.password
        self.token = base64.b64encode(credentials.encode()).decode('utf-8')
        

    def activate_plugin(self, plugin_slug, site) -> str:
        p = subprocess.run(f"wp plugin activate {plugin_slug} --path=/var/www/html --url=https://blogs-dev.butler.edu{site}", shell=True, capture_output=True)
        # print(p.stdout)
        print(f"{Fore.GREEN}{plugin_slug} was activated on {site}")
        return p.stdout
    

    def get_user_blogs(self, user_blogs, mysql) -> None: 
        """Gets all the blog ids and blog paths.

        Args:
            user_blogs (_type_): _description_
            mysql (_type_): _description_
        """        
        cursor = mysql.cursor()

        query = ('''select blog_id, path from wp_blogs''')
        cursor.execute(query)

        for(blog_id, path) in cursor:
            user_blogs [blog_id] = path
        
        cursor.close()