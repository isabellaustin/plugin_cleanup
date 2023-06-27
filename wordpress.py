from typing import List
import base64
from colorama import Fore, Back
import subprocess
from phpserialize import *
import json

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
        

    def activate_plugin(self, plugin, site, site_id,cnx) -> str:
        plugin_slug = wp.get_plugin_slug(self,plugin,site_id,cnx)
        if plugin_slug != "":
            p = subprocess.run(f"wp plugin activate {plugin_slug} --path=/var/www/html --url=https://blogs-dev.butler.edu{site}", shell=True, capture_output=True)
            # print(p.stdout)
            print(f"{Fore.GREEN}{plugin_slug} was activated on {site}")
            return p.stdout
    

    def deactivate_plugin(self, plugin_slug, site) -> str:
        p = subprocess.run(f"wp plugin deactivate {plugin_slug} --path=/var/www/html --url=https://blogs-dev.butler.edu{site}", shell=True, capture_output=True)
        # print(p.stdout)
        print(f"{Fore.GREEN}{plugin_slug} was deactivated on {site}")
        return p.stdout


    def get_plugin_slug(self, plugin, site_id:int, mysql) -> str:
        cursor = mysql.cursor()
        
        query = ('select option_value from wp_%s_options where option_name = "active_plugins"')
        cursor.execute(query, (site_id,))

        results = cursor.fetchall()
        site_plugins = []

        for r in results: #creates a list of the site's activated plugins 
            data = r[0]
            plugin_dict = loads(data.encode())
            for p in plugin_dict.keys():
                plugin_name = plugin_dict[p].decode() #'classic-editor/classic-editor.php'
                slug = plugin_name.split("/")[0]
                site_plugins.append(slug)
        # print(list(plugin_dict.values()))

        data = plugin
        pl = loads(data.encode())
        # IF-ELSE: OPPOSITE FOR DEACTIVATE
        if pl[0] not in list(plugin_dict.values()): #checks if suggested plugin is already activated
            slug = pl[0].decode()
            plugin_slug = slug.split("/")[0]

            cursor.close()

            return plugin_slug
        else:
            slug = pl[0].decode()
            plugin_slug = slug.split("/")[0]
            print(f"{Fore.GREEN}{plugin_slug} was already active{Fore.RESET}")

            cursor.close()

            return ""


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