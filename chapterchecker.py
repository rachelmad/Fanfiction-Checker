from lxml import html
import requests
import pickle
from datetime import date
import sys

class ChapterChecker:
    def __init__(self):
        self.stories = []
        self.favorites = []
        self.update_self_stories()
        self.show_updates()
        
    # Program assumes this function works
    def story_page_exists(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        status = tree.xpath('//div[@id="storytext"]/text()')
        return len(status) != 0

    #------------------------ Manipulating Self ------------------------#
    def update_self_stories(self):
        try:
            file = open('stories.pydata', 'rb')
            self.stories = pickle.load(file)
            file.close()
        except Exception as e:
            print e
            self.stories = []
        
    def update_self_favorites(self):
        try:
            file = open('favorites.pydata', 'rb')
            self.favorites = pickle.load(file)
            file.close()
        except Exception as e:
            print e
            self.favorites = []
        
    def find_story(self, story_number):
        for story in self.stories:
            if story[0] == story_number:
                return story
        return None
        
    #------------------------ Main Options ------------------------#
    def view_incomplete_stories(self):
        self.view_stories(self.stories)
        
    def view_favorites(self):
        if self.favorites != []:
            self.print_urls(self.favorites)
        else:
            self.update_self_favorites()
            self.print_urls(self.favorites)
    
    def view_stories(self, story_list):
        for story in story_list:
            print ', '.join(map(str, story))
            
    def add_incomplete_story(self):
        story_number = self.get_story_number()
        chapter = self.get_chapter_number(story_number)
        self.add_story(story_number, chapter, self.stories)
        
    def add_favorite(self, story_number):
        if self.favorites != []:
            self.add_story(story_number, 1, self.favorites)
        else:
            self.update_self_favorites()
            self.add_story(story_number, 1, self.favorites)
        
    def add_story(self, story_number, chapter, to_update):
        url = self.make_url(story_number, chapter)        
        title = self.get_title(url) 
        last_read = str(date.today())   
        to_update.append([story_number, title, chapter, last_read])
        
    def get_updated_stories(self):
        updated = []
        for story in self.stories:
            if (self.is_story_updated(story)):
                updated.append(story)
        return updated
        
    def print_urls(self, story_list):
        for story in story_list:
            print story[1], self.make_url(story[0], story[2] + 1)
            
    def delete_story(self, story_number):
        story = self.find_story(story_number)
        if (story is not None):
            self.stories.remove(story) 
                
    def edit_story_chapter(self):
        story_number = self.get_story_number()
        self.delete_story(story_number)
        chapter = self.get_chapter_number(story_number)
        self.add_story(story_number, chapter, self.stories)
    
    def show_updates(self):
        updated = self.get_updated_stories()
        self.print_urls(updated)
        if updated != []:
            update = self.get_update_option(updated)
            if update == 1:
                self.update_list(updated)
        
    def move_to_favorites(self):
        story_number = self.get_story_number()
        self.delete_story(story_number)
        self.add_favorite(story_number)
        
    def update_list(self, story_list):
        for story in story_list:
            story_number = story[0]
            chapter = story[2] + 1
            self.delete_story(story_number)
            self.add_story(story_number, chapter, self.stories)
            
    #------------------------ Get From User ------------------------#
    def get_title(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        title = str(tree.xpath('//b[@class="xcontrast_txt"]/text()'))
        return title
    
    def get_story_number(self):
        story_exists = False
        while (not story_exists):
            story_number = input('Enter story number: ')
            story_exists = self.check_story_exists(story_number)
        return story_number
        
    def get_chapter_number(self, story_number):
        chapter_number = 0
        chapter_exists = False
        while (chapter_number < 1 or not chapter_exists):
            chapter_number = input('Enter last chapter read: ')
            url = self.make_url(story_number, chapter_number)
            chapter_exists = self.check_chapter_exists(story_number, chapter_number)
        return chapter_number
        
    def get_update_option(self, story_list):
        update_all = -1
        while (update_all < 0):
            update_all = input('Update all (0/1)? ')
            if not (update_all == 0 or update_all == 1):
                update_all = -1
        return update_all
            
    #------------------------ Manipulating Files ------------------------#                   
    def save_stories(self):
        try:
            file = open('stories.pydata', 'wb')            
            pickle.dump(self.stories, file)            
            file.close()            
            if self.favorites != []:
                file2 = open('favorites.pydata', 'wb')
                pickle.dump(self.favorites, file2)
                file2.close()
        except Exception as e:
            print e
        
    #------------------------ Website Functions ------------------------#          
    def check_story_exists(self, number):
        url = 'https://www.fanfiction.net/s/' + str(number) + '/1'
        return self.story_page_exists(url)
        
    def make_url(self, story, chapter):
        url = 'http://www.fanfiction.net/s/' + str(story) + '/' + str(chapter)
        return url
        
    def check_chapter_exists(self, story, chapter):
        url = 'http://www.fanfiction.net/s/' + str(story) + '/' + str(chapter)
        return self.story_page_exists(url)
       
    def is_story_updated(self, story):
        url = self.make_url(story[0], story[2] + 1)
        return self.story_page_exists(url)       
            
            
if __name__ == '__main__':
    checker = ChapterChecker()

    while (True):
        print '1. Check updates'
        print '2. View incomplete stories'
        print '3. View completed favorites'
        print '4. Add story'
        print '5. Edit chapter'
        print '6. Delete story'
        print '7. Move story to finished'
        print '8. Exit'
        choice = input ("Choose option: ")

        if (choice == 1):
            checker.show_updates()
        elif (choice == 2):
            checker.view_incomplete_stories()
        elif (choice == 3):
            checker.view_favorites()
        elif (choice == 4):
            checker.add_incomplete_story()
        elif (choice == 5):
            checker.edit_story_chapter()
        elif (choice == 6):
            checker.delete_story(checker.get_story_number())
        elif (choice == 7):
            checker.move_to_favorites()
        elif (choice == 8):
            checker.save_stories()
            sys.exit()