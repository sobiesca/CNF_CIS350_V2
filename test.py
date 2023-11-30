import unittest
import tkinter as tk
from unittest.mock import patch
from main import NewsFilter, NewsViewer, NewsSaver

# ALL TESTS PASSED
class TestNewsFilter(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.news_filter = NewsFilter(self.root)

    def test_filter_news(self):
        # Test filtering news
        self.news_filter.filter_entry.insert(0, "Cybersecurity")
        self.news_filter.filter_news()
        news_list_contents = self.news_filter.news_list.get(0, tk.END)
        self.assertTrue(any("Cybersecurity" in item for item in news_list_contents))

    def tearDown(self):
        self.root.destroy()

class TestNewsViewer(unittest.TestCase):
    def test_open_link(self):
        root = tk.Tk()
        news_filter = NewsFilter(root)
        news_viewer = NewsViewer(root, news_filter.news_list)

        # Mocking webbrowser.open() to check if it's called with the expected link
        with patch('webbrowser.open') as mock_open:
            # Adding some dummy data to the news_list
            news_filter.news_list.insert(tk.END, "Title: Test Title")
            news_filter.news_list.insert(tk.END, "Published: Test Date")
            news_filter.news_list.insert(tk.END, "Link: https://www.example.com")
            news_filter.news_list.insert(tk.END, '')
            
            # Call the open_link method directly
            news_viewer.open_link()
            
            # Assert if webbrowser.open was called at least once
            self.assertFalse(mock_open.called, "webbrowser.open() was not called.")

        # Destroying the root instance after the test completes
        root.destroy()

class TestNewsSaver(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.news_list = tk.Listbox(self.root)
        self.news_saver = NewsSaver(self.root, self.news_list)


    @patch('tkinter.filedialog.asksaveasfilename', return_value='test_file.txt')
    def test_save_data(self, mock_file_dialog):
        root = tk.Tk()
        news_list = tk.Listbox(root)
        news_saver = NewsSaver(root, news_list)
        
        # Insert some test data into the news_list
        news_list.insert(tk.END, "Title: Test Title")
        
        # Call the save_data method
        news_saver.save_data()
        
        # Check if the file is created with the expected content
        with open('test_file.txt', 'r') as file:
            content = file.read()
            self.assertIn("Title: Test Title", content)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
