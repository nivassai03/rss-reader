import sys
from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint
from PySide6.QtGui import QAction,QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QHBoxLayout,QSizePolicy,QSplitter,QToolBar
from gui import AddSourceAction, ArticlesListWidget, RefreshAction,SourceTreeWidget,ArticleWebView

def parse_source():
    with open("sources.json","r") as f:
        sources = json.load(f)
    return sources


def parse_xml(url):
    xml_source = requests.get(url)
    parsed_xml = BeautifulSoup(xml_source.content,features="xml")
    return parsed_xml


def get_feed_items(url):
    feed_list = []
    parsed_xml = parse_xml(url)
    parsed_items = parsed_xml.find_all('item')
    # for item in parsed_items:
    #     news = dict()
    #     news['title'] = item.contents[0].string
    #     news['description'] = item.contents[1].string
    #     news['link'] = item.contents[2].string
    #     news['date'] = item.contents[4].string
    #     news_list.append(news)
    # return news_list
    for item in parsed_items:
        feed = dict()
        for item_children in item.children:
            if(item_children.name == 'title'):
                feed['title'] = item_children.string
            elif(item_children.name == 'description'):
                feed['description'] = item_children.string
            elif(item_children.name == 'link'):
                feed['link'] = item_children.string
            elif(item_children.name == 'pubDate'):
                feed['pubDate'] = item_children.string
        feed_list.append(feed)
    return feed_list

def get_entire_feed_list(sources):
    feed_list = dict()
    for catogery in sources.keys():
        for source in sources[catogery]:
            source_name = source['Name']
            source_url = source['url']
            feed_items = get_feed_items(source_url)
            if catogery not in feed_list.keys():
                feed_list[catogery] = {source_name:feed_items}
            else:
                feed_list[catogery].update({source_name:feed_items})
    return feed_list

sources = parse_source()
feed_data = get_entire_feed_list(sources)
print(feed_data)

# with open("feed.json","w") as f:
#     json.dump(feed_data,f,indent=2)


# def generate_source_tree_data(feed_data):
#     source_tree_data = dict()
#     for category in feed_data.keys():
#         source_tree_data[category] = list(feed_data[category].keys())
#     return source_tree_data

# def get_article_list(feed_data,category,source_name):
#     return feed_data[category][source_name]

# source_tree_data = generate_source_tree_data(feed_data)

class MainWindow(QMainWindow):
    def __init__(self,feed_data):
        super().__init__()
        self.setWindowTitle("RSS READER")
        self.feed_data = feed_data
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        add_source_action = AddSourceAction(self,self.feed_data)
        toolbar.addAction(add_source_action)
        self.addToolBar(toolbar)
        self.source_tree = SourceTreeWidget(self.feed_data)
        self.articles_list = ArticlesListWidget(self.feed_data)
        self.source_tree.source_selected.connect(self.articles_list.update_articles_list)
        #article_display_tab = ArticleTabDisplay()
        self.article_web_view = ArticleWebView()
        self.articles_list.article_cliked.connect(self.article_web_view.load_url)
        self.articles_list.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.source_tree.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #article_display_tab.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.article_web_view.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum)
        layout = QHBoxLayout()
        splitter_layout = QSplitter()
        splitter_layout.addWidget(self.source_tree)
        splitter_layout.addWidget(self.articles_list)
        # layout.addWidget(article_display_tab)
        splitter_layout.addWidget(self.article_web_view)
        splitter_layout.setContentsMargins(0,0,0,0)
        layout.addWidget(splitter_layout)
        layout.setContentsMargins(0,0,0,0)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow(feed_data)
window.show()
sys.exit(app.exec())
