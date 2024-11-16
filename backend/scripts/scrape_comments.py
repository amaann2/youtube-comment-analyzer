from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
class SeleniumProcessor:
    def __init__(self):
        self.browser = None
        self.options = Options()
        self.options.add_argument("--headless")  
        self.options.add_argument("--start-maximized")

    def start_browser(self):
        """Starts the browser if not already started."""
        if not self.browser:
            self.browser = webdriver.Chrome(options=self.options)
        return self.browser

    def close_browser(self):
        """Closes the browser and resets the instance."""
        if self.browser:
            self.browser.quit()
            self.browser = None

    def load_url(self, url):
        """
        Loads the specified URL in the browser.
        Args:
            url: The URL to load.
        """
        self.start_browser()
        self.browser.get(url)
        time.sleep(5)  
    def extract_total_comments_count(self):
        """
        Extracts the total number of comments available on the YouTube video.
        Returns:
            int: Total number of comments.
        """
        try:
            # Locate the total comment count element
            total_count_element = self.browser.find_element(
                By.CSS_SELECTOR, "ytd-comments-header-renderer #count yt-formatted-string span"
            )
            # Extract the text, remove commas, and convert to integer
            total_count_text = total_count_element.text.replace(",", "")
            return int(total_count_text)
        except Exception as e:
            print(f"Could not fetch total comments count: {e}")
            return 0


    def extract_comments(self, comments_per_scroll=20):
        """
        Extracts comments from the YouTube video page.
        Args:
            scroll_limit: Number of times to scroll to load more comments.
        Returns:
            List of unique comments.
        """
        try:
            if not self.browser:
                raise Exception("Browser is not initialized. Call `load_url` first.")

            wait = WebDriverWait(self.browser, 5)
            comments = set()

            total_comments_count = self.extract_total_comments_count()
            if total_comments_count == 0:
                print("No comments found on the video.")
                
            
            scroll_limit  = (total_comments_count // comments_per_scroll) + 1
            print(f"Estimated scroll limit: {scroll_limit} for {total_comments_count} comments.")


            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//ytd-item-section-renderer[@id='sections']")
                )
            )

            last_height = self.browser.execute_script("return document.documentElement.scrollHeight")

            for _ in range(scroll_limit):
                self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(2) 

                comment_elements = self.browser.find_elements(
                    By.CSS_SELECTOR, "ytd-comment-thread-renderer"
                )

                for comment_element in comment_elements:
                    try:
                        comment_text_element = comment_element.find_element(
                            By.CSS_SELECTOR, "ytd-expander #content-text"
                        )
                        comment_html = comment_text_element.get_attribute("innerHTML").strip()
                        soup = BeautifulSoup(comment_html, "html.parser")
                        for img in soup.find_all("img"):
                            emoji = img.get("alt", "")  
                            img.replace_with(emoji) 
                        # comment_text_with_emojis = soup.get_text(strip=True)
                        comment_text_with_emojis = "".join(soup.stripped_strings)

                        author_element = comment_element.find_element(
                            By.CSS_SELECTOR, "#header-author #author-text span"
                        )
                        author_name = author_element.text.strip()
                        
                        # Extract post date
                        date_element = comment_element.find_element(
                            By.CSS_SELECTOR, "#header-author #published-time-text a"
                        )
                        post_date = date_element.text.strip()
                        # comments.add(comment_text_with_emojis)
                        comments.add((author_name, post_date, comment_text_with_emojis))
                    except Exception:
                        continue

                # Check if more content was loaded
                new_height = self.browser.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break  # Stop scrolling if no new content is loaded
                last_height = new_height


            return list(comments) 
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

if __name__ == "__main__":
    processor = SeleniumProcessor()
    try:
        video_url = "https://www.youtube.com/watch?v=yl6yufvcQmg"  
        processor.load_url(video_url)
        start_time = time.time()
        comments = processor.extract_comments()
        end_time = time.time()
        print(f"Total time taken: {end_time - start_time:.2f} seconds")
        print(f"Extracted {len(comments)} comments:")
        if comments:
            df= pd.DataFrame(comments, columns=['author', 'date', 'comment'])
            df.to_csv('comments.csv', index=False)
            print("Comments saved to comments.csv")
    finally:
        processor.close_browser()
