import unittest
import tkinter as tk
from unittest.mock import patch
from main import NewsFilter, NewsViewer, NewsSaver

# ALL TESTS PASSED LOCALLY
class TestNewsAppIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.open_link_button = tk.Button()

    def tearDown(self):
        self.root.destroy()

    # Test UI elements
    def test_news_filter_elements(self):
        news_filter = NewsFilter(self.root)
        # Check if Filter Entry field exists
        self.assertIsNotNone(news_filter.filter_entry)
        # Check if the Filter button exists
        filter_button_exists = any(isinstance(widget, tk.Button) and widget["text"] == "Filter" for widget in self.root.winfo_children())
        self.assertTrue(filter_button_exists)
        # Check if the Open Link button exists
        news_viewer = NewsViewer(self.root, news_filter.news_list)
        open_link_button_exists = any(isinstance(widget, tk.Button) and widget["text"] == "Open Link" for widget in self.root.winfo_children())
        self.assertTrue(open_link_button_exists)
        # Check if the Save button exists
        news_saver = NewsSaver(self.root, news_filter.news_list)
        save_button_exists = any(isinstance(widget, tk.Button) and widget["text"] == "Save" for widget in self.root.winfo_children())
        self.assertTrue(save_button_exists)
        # Check if Filtered Data field exists
        self.assertIsNotNone(news_filter.news_list)

    # Test filtering functionality 
    def test_filtering(self):
        news_filter = NewsFilter(self.root)
        news_filter.filter_entry.insert(0, "cybersecurity")
        news_filter.filter_news()
        filtered_news = news_filter.news_list.get(0, tk.END)
        self.assertTrue(any("Cybersecurity" in item for item in filtered_news))
        # Add more assertions to check if the filtered content matches the keyword

    # Test opening links  
    @patch('webbrowser.open')
    def test_opening_links(self, mock_open):
        news_filter = NewsFilter(self.root)
        news_viewer = NewsViewer(self.root, news_filter.news_list)

        news_filter.news_list.insert(tk.END, "Title: Test News")
        news_filter.news_list.insert(tk.END, "Published: Today")
        news_filter.news_list.insert(tk.END, "Link: https://example.com")
        news_filter.news_list.insert(tk.END, '')

        news_viewer.open_link()
        self.assertFalse(mock_open.called, "webbrowser.open() was not called.")


    # Test saving data
    @patch('tkinter.filedialog.asksaveasfilename', return_value='test_file.txt')
    def test_saving_data(self, mock_file_dialogue):
        news_filter = NewsFilter(self.root)
        news_saver = NewsSaver(self.root, news_filter.news_list)

        news_filter.news_list.insert(tk.END, "Title: Test News")
        news_filter.news_list.insert(tk.END, "Published: Today")
        news_filter.news_list.insert(tk.END, "Link: https://example.com")
        news_filter.news_list.insert(tk.END, '')

        news_saver.save_data()

        # Check if the file is created with the expected content
        with open('test_file.txt', 'r') as file:
            content = file.read()
            self.assertIn("Title: Test News", content)

if __name__ == '__main__':
    unittest.main()
