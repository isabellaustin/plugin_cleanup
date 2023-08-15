import base64
from colorama import Fore
import subprocess
from phpserialize import *

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


    def activate_plugin(self, plugin: str, site: str, site_id: int,logger,cnx) -> None:
        """Activates a desired plugin on every site in a mutlisite network

        Args:
            plugin (str): string for desired plugin for activation
            site (str): the site slug/path that the plugin is being activated on
            site_id (int): the site id that the plugin is being activated on
            logger (logging.Logger): log the success/failure messages of each sites activation
            cnx (connector): SQL connection
        """        
        plugin_slug = wp.get_plugin_slug(self,plugin,site_id,cnx) 

        for slug in list(plugin_slug.keys()): #should only have one key
            is_active = plugin_slug[slug]

            if is_active:
                print(f"{Fore.RED}{slug} was already active on {site}{Fore.RESET}")
                logger.info(f"{site}: {slug} was already active")
            else:
                p = subprocess.run(f"wp plugin activate {slug} --path=/var/www/html --url=https://blogs-dev.butler.edu{site}", shell=True, capture_output=True)
                status = p.stdout
                print(f"{Fore.GREEN}{slug} was activated on {site}{Fore.RESET}")
                logger.info(f"{site}: {status.decode()}")
 

    def deactivate_plugin(self, plugin: str, site: str, site_id: int,logger,cnx) -> None:
        """Deactivates a desired plugin on every site in a mutlisite network

        Args:
            plugin (str): string for desired plugin for activation
            site (str): the site slug/path that the plugin is being activated on
            site_id (int): the site id that the plugin is being activated on
            logger (logging.Logger): log the success/failure messages of each sites activation
            cnx (connector): SQL connection
        """        
        plugin_slug = wp.get_plugin_slug(self,plugin,site_id,cnx)

        for slug in list(plugin_slug.keys()):
            is_active = plugin_slug[slug]

            if is_active:
                p = subprocess.run(f"wp plugin deactivate {slug} --path=/var/www/html --url=https://blogs-dev.butler.edu{site}", shell=True, capture_output=True)
                status = p.stdout
                print(f"{Fore.GREEN}{slug} was deactivated on {site}{Fore.RESET}")
                logger.info(f"{site}: {status.decode()}")
            else:
                print(f"{Fore.RED}{slug} was already inactive on {site}{Fore.RESET}")
                logger.info(f"{site}: {slug} was already inactive")


    def get_plugin_slug(self, plugin: str, site_id: int, mysql) -> dict[str, bool]:
        """ Determines if the desired plugin (classin-editor) and is already 
            active on a certian site in the multisite network or not

        Args:
            plugin (str): string for desired plugin for activation
            site_id (int): the site id that the plugin is being activated on
            mysql (connector): SQL connection

        Returns:
            dict[str, bool]: Returns dict of a certain site and if the desired plugin is already 
            active on it or not
        """        
   
        cursor = mysql.cursor()
        
        query = ('select option_value from wp_%s_options where option_name = "active_plugins"')
        cursor.execute(query, (site_id,))

        results = cursor.fetchall()
        site_plugins = []
        slug_status = {}

        for r in results: #creates a list of the site's activated plugins 
            data = r[0]
            plugin_dict = loads(data.encode())
            for p in plugin_dict.keys():
                plugin_name = plugin_dict[p].decode() #'classic-editor/classic-editor.php'
                slug = plugin_name.split("/")[0]
                site_plugins.append(slug)

        data = plugin
        plugins = loads(data.encode())
        for p in plugins:
            slug = plugins[p].decode()
            plugin_slug = slug.split("/")[0]

            #checks if suggested plugin is already activated
            if plugins[p] not in list(plugin_dict.values()): 
                slug_status[plugin_slug] = False #NOT IN LIST; inactive
            elif plugins[p] in list(plugin_dict.values()):
                slug_status[plugin_slug] = True #IN LIST; active
        
        cursor.close()
        return slug_status


    def get_user_blogs(self, user_blogs: dict[int, str], mysql) -> None: 
        """Gets all the blog ids and blog paths.

        Args:
            user_blogs (dict[int, str]): a dict of blogs in the database
            mysql (connector): SQL connection
        """        
        cursor = mysql.cursor()

        query = ('''select blog_id, path from wp_blogs''')
        cursor.execute(query)

        for(blog_id, path) in cursor:
            user_blogs [blog_id] = path
        
        cursor.close()