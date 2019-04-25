import hashlib
import os
import random
import tempfile
import zipfile
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from . import utils

PROXY_TEMPLATE = 'https://lum-customer-hl_a3dca943-zone-static-session-{session_id}:wbuavmmsjwg9@zproxy.lum-superproxy.io:22225'


def get_proxies(enable=True):
    if not enable:
        return None

    proxy = PROXY_TEMPLATE.format(session_id=random.randrange(10000, 99999))

    return {
        'http': proxy,
        'https': proxy,
    }


class ChromeExtension(object):
    """Create a chrome extension that will automatically auth proxy"""

    def __init__(self, proxy_config, extension_name='proxy_auth_plugin.zip'):
        self.proxy_config = proxy_config
        self.extension_name = '%s_%s' % (utils.unique_string(), extension_name)

    @property
    def manifest_json(self):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        return manifest_json

    @property
    def background_js(self):
        background_js = """
        var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%(host)s",
                port: parseInt(%(port)s)
              },
              bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        chrome.webRequest.onAuthRequired.addListener(
            function(details, callbackFn) {
                var auth = {authCredentials: {username: "%(username)s", password: "%(password)s"}};
                //console.log("onAuthRequired!", details, auth);
                callbackFn(auth);
            },
            {urls: ["<all_urls>"]},
            ['asyncBlocking']
        );
        """ % self.proxy_config

        return background_js

    def create_extension_archive(self):
        extension_path = os.path.join(tempfile.mkdtemp(), self.extension_name)

        if not os.path.exists(extension_path):
            with zipfile.ZipFile(extension_path, 'w') as zp:
                zp.writestr("manifest.json", self.manifest_json)
                zp.writestr("background.js", self.background_js)

        return extension_path


def get_webdriver(account, auth_extension=True):
    session_id = hashlib.md5(account['username'].encode('utf-8')).hexdigest()
    proxy = PROXY_TEMPLATE.format(session_id=session_id)
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent=\"{account['ua']}\"")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

        if auth_extension:
            urlp = urlparse(proxy)
            proxy_config = {
                'host': urlp.hostname,
                'port': urlp.port,
                'username': urlp.username,
                'password': urlp.password
            }
            options.add_extension(ChromeExtension(proxy_config).create_extension_archive())

    driver = webdriver.Remote(command_executor='http://hub:4444/wd/hub',
                              desired_capabilities=desired_capabilities, options=options)
    return driver
