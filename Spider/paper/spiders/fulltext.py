import scrapy
from scrapy_playwright.page import PageMethod
from paper.items import PaperItem
import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

ELSAPIKEY = os.environ.get('ELSAPIKEY')


class FullSpider(scrapy.Spider):
    name = 'full'

    async def start(self):
        
        df = pd.read_excel('Filter_1.xlsx')
        filte = pd.read_csv('File_name.csv',header=None)
        drop_list = filte[0].to_list()

        doi_list_ = df['DOI']
        publisher_list_ = df['Publisher']
        
        to_do = []

        for doi,pub in zip(doi_list_,publisher_list_):
            
            if doi in drop_list:

                self.logger.info(f"DOI:{doi}\t Publisher:{pub} Over")
                continue
            
            to_do.append((doi,pub))
    

        for doi,pub in to_do:
            self.logger.info("Loading REQUESTS")
            self.logger.info(f"DOI:{doi}\t Publisher:{pub}")

            if doi in drop_list:

                self.logger.info(f"DOI:{doi}\t Publisher:{pub} Over")
                continue

            
            if pub == 'ELSEVIER':
                
                url = f'https://api.elsevier.com/content/article/doi/{doi}'
                self.logger.info(f"Loading Schedule {url}")
                

                yield scrapy.Request(
                    url=url,
                    headers = {"X-ELS-APIKey": ELSAPIKEY},
                    meta={
                        'doi':doi
                    },
                    callback=self.save_xml,
                    dont_filter=False,
                    errback=self.error_callback
                )

            elif pub == 'ROYAL SOC CHEMISTRY':

                
                url = f'https://pubs.rsc.org/doi/{doi}'
                self.logger.info(f"Loading Schedule {url}")

                yield scrapy.Request(
                    url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": "logged_in",
                        "check_login": False,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector","#divWelcomeUser > span", timeout=300000),
                            PageMethod("add_init_script", script="delete Object.getPrototypeOf(navigator).webdriver"),
                            PageMethod("wait_for_selector", ".ref-list", timeout=300000),
                            PageMethod("wait_for_timeout", 2000),
                        ],
                        'doi':doi
                    },
                    callback=self.save_page,
                    dont_filter=False,
                    errback=self.error_callback
                )

            elif pub == 'AMER CHEMICAL SOC':

                
                url = f'https://pubs.acs.org/doi/{doi}'
                self.logger.info(f"Loading Schedule {url}")

                yield scrapy.Request(
                    url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("add_init_script", script="delete Object.getPrototypeOf(navigator).webdriver"),
                            PageMethod("wait_for_selector", ".article_fullPage h1", timeout=30000),
                            # PageMethod("wait_for_function", """
                            #             () => document.querySelector('.hlFld-Title') || 
                            #                 document.body.innerText.includes('https://doi.org/')
                            #         """, timeout=30000),
                            
                            PageMethod("wait_for_timeout", 2000),
                            
                        ],
                        'doi':doi
                    },
                    callback=self.save_page,
                    dont_filter=False,
                    errback=self.error_callback
                )

    async def save_page(self, response):
        """
        Save html page
        """
        self.logger.info(f"Request received: {response.url} (Status: {response.status})")
        page = response.meta["playwright_page"]
        try:
            os.makedirs("Fulltext", exist_ok=True)
            
            filename = f"{response.url.split('/')[-1]}.html"
            path = f"Fulltext/{filename}"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            item = PaperItem()
            item['doi'] = response.meta['doi']
            item['file_name'] = filename
            item['file_type'] = 'html'
            yield item

            self.logger.info(f"{response.meta['doi']} to HTML Saved: {path}")

        except Exception as e:
            self.logger.error(f" Page Error: {e}", exc_info=True)
        finally:
            await page.close()

    async def save_xml(self,response):

        if response.status == 200:
            os.makedirs("Fulltext", exist_ok=True)
            filename = f"{response.meta['doi'].replace('/', '_')}.xml"
            path = f"Fulltext/{filename}"
            with open(path, "wb") as f:
                f.write(response.body)

            item = PaperItem()
            item['doi'] = response.meta['doi']
            item['file_name'] = filename
            item['file_type'] = 'xml'
            yield item
            self.logger.info(f"{response.meta['doi']} to XML Saved {path}")

        else:
            self.logger.info(f"Failed to fetch {response.url}")

    def error_callback(self, failure):
        """Request Error"""
        self.logger.info(f"Failure Value: {failure.value}")
        self.logger.info(f"URL: {failure.request.url}")
        self.logger.info(f"Failure Type: {failure.type}")
        self.logger.info(f"Traceback: {failure.getTraceback()}")
