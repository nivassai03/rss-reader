import json
from PySide6.QtCore import QVersionNumber, Qt,QUrl,Signal,Slot
from PySide6.QtGui import QAction, QPixmap,QIcon
from PySide6.QtWidgets import QDialog, QWidget,QTreeWidget,QTreeWidgetItem,QTableWidget,QTableWidgetItem,QHBoxLayout,QListWidget,QListWidgetItem,QVBoxLayout,QLabel,QSizePolicy,QTabWidget,QDialogButtonBox,QFormLayout,QComboBox,QLineEdit,QMainWindow,QCheckBox
from PySide6.QtWebEngineWidgets import QWebEngineView

# class ArticleTabDisplay(QTabWidget):

#     def __init__(self):
#         super().__init__()
#         self.addTab(QLabel("Tab1"),"1")
#         self.addTab(QLabel("Tab2"),"2")
#         self.addTab(QLabel("Tab3"),"3")


class AddSourceDialog(QDialog):

    def __init__(self,parent,category_list):
        print("Dialog: Parent",type(parent),parent)
        super().__init__(parent)
        self.setWindowTitle("Add Source")
        self.source_category = ""
        self.is_category_new = False
        self.source_url = ""
        self.source_name = ""
        self.add_source_form_layout = QFormLayout()
        self.category_select = QComboBox()
        self.new_category_name = QLineEdit()
        self.new_source = QLineEdit()
        self.new_url = QLineEdit()
        self.category_select.setPlaceholderText("")
        self.category_select.addItem("")
        self.category_select.addItems(category_list)
        self.category_select.currentTextChanged.connect(self.add_new_category)
        self.category_select.addItem("Other")
        self.add_source_form_layout.insertRow(0,"Select Categroy",self.category_select)
        self.add_source_form_layout.insertRow(1,"Enter New Category",self.new_category_name)
        self.add_source_form_layout.setRowVisible(1,False)
        self.add_source_form_layout.insertRow(2,"Enter Source Name",self.new_source)
        self.add_source_form_layout.insertRow(3,"Enter Url",self.new_url)
        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.add_source_form_layout.insertRow(4,self.button_box)
        self.button_box.accepted.connect(self.add_new_source)
        self.button_box.rejected.connect(self.close)
        self.setLayout(self.add_source_form_layout)

    def add_new_category(self,s):
        if s == 'Other':
            self.add_source_form_layout.setRowVisible(1,True)
            self.is_category_new = True

        else:
            self.source_category = self.category_select.currentText()

    def add_new_source(self):
        if self.is_category_new:
            self.source_category = self.new_category_name.text()
        self.source_name = self.new_source.text()
        self.source_url = self.new_url.text()
        print(repr(self.source_category),repr(self.source_name),repr(self.source_url))
        if self.source_category != "" and self.source_name != "" and self.source_url != "":
            with open("sources.json","r") as read_source_file:
                sources = json.load(read_source_file)
            if self.source_category in sources.keys():
                sources[self.source_category].append(
                    {
                        "Name":self.source_name,
                        "url":self.source_url
                    }
                )
            else:
                sources.update({self.source_category:[{"Name":self.source_name,"url":self.source_url}]})
                print(sources)
            with open("sources.json","w") as write_source_file:
                json.dump(sources,write_source_file,indent=4)
            self.close()
        else:
            self.close()





class AddSourceAction(QAction):

    feed_data = {}

    def __init__(self,parent,feed_data):
        super().__init__(parent)
        print("Actin: Parent",type(parent),parent)
        self.feed_data = feed_data
        self.parent = parent
        self.setText("Add Source")
        self.setStatusTip("Add Source")
        self.setIcon(QIcon("img/icons/add.png"))
        self.triggered.connect(self.open_add_source_dialog)

    @Slot()
    def open_add_source_dialog(self):
        category_list = list(self.feed_data.keys())
        dlg = AddSourceDialog(self.parent,category_list)
        dlg.exec()


class RefreshAction(QAction):
    def __init__(self,parent):
        super().__init__(parent)
        self.setText("Refresh Feed")
        self.setStatusTip("Refresh Feed")
        self.setIcon(QIcon('img/icons/refresh.png'))


class ArticleWebView(QWebEngineView):

    def __init__(self):
        super().__init__()
        initialUrl = ''
        self.load(QUrl(initialUrl))

    @Slot(QUrl)
    def load_url(self,article_url):
        self.load(QUrl(article_url))


# class ArticlesTableWidget(QTableWidget):

#     def __init__(self,articles):
#         super().__init__()
#         self.setShowGrid(False)
#         self.setRowCount(len(articles))
#         self.setColumnCount(2)
#         self.setHorizontalHeaderLabels(["Title","Author","Date"])
#         self.construct_articles_table(articles)

#     def construct_articles_table(self,articles):
#         for i,(title,author,date) in enumerate(articles):
#             print(i,title,author,date)
#             article_name = QTableWidgetItem(title)
#             article_author = QTableWidgetItem(author)
#             article_date = QTableWidgetItem(date)
#             self.setItem(i,-1,article_name)
#             self.setItem(i,0,article_author)
#             self.setItem(i,1,article_date)

class ArticlesListWidgetItem(QWidget):
    def __init__(self,article):
        super().__init__()
        # source_name = "Debian"
        content_layout = QVBoxLayout()
        side_icon_layout = QVBoxLayout()
        widget_layout = QHBoxLayout()
        #content_header_layout = QHBoxLayout()
        title_label = article['title'][:100]+'...'
        description_label = article['description'][:100]+'...'
        self.title = QLabel(title_label)
        self.link = article['link']
        self.description = QLabel(description_label)
        self.description.setWordWrap(True)
        self.date = QLabel(article['pubDate'])
        # self.source = QLabel(source_name)
        #content_header_layout.addWidget(self.source,Qt.AlignLeft)
        #content_header_layout.addWidget(self.date,Qt.AlignRight)
        #content_layout.addLayout(content_header_layout)
        content_layout.addWidget(self.date)
        content_layout.addWidget(self.title)
        content_layout.addWidget(self.description)
        article_icon_pixmap = QPixmap('img/icons/article.png').scaled(20,20)
        article_icon = QLabel()
        article_icon.setPixmap(article_icon_pixmap)
        article_icon.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        side_icon_layout.addWidget(article_icon)
        widget_layout.addLayout(side_icon_layout)
        widget_layout.addLayout(content_layout,Qt.AlignLeft)
        widget_layout.setSpacing(10)
        self.setLayout(widget_layout)


    def get_article_data(self):
        return {
            'link':self.link,
        }


class ArticlesListWidget(QListWidget):

    feed_data = {}

    def __init__(self,feed_data):
        super().__init__()
        self.articles = []
        ArticlesListWidget.feed_data = feed_data
        self.itemClicked.connect(self.display_article)

    article_cliked = Signal(str)

    @Slot(QListWidgetItem)
    def display_article(self,item):
        article_link = self.itemWidget(item).get_article_data()['link']
        self.article_cliked.emit(article_link)

    def get_article_list(self,feed_data,category,source_name):
            return feed_data[category][source_name]

    @Slot(str,str)
    def update_articles_list(self,category,source_name):
        self.clear()
        self.articles = self.get_article_list(ArticlesListWidget.feed_data,category,source_name)
        self.construct_articles_list(self.articles)
        self.setMinimumWidth(self.sizeHintForColumn(0)+20)

    def construct_articles_list(self,articles):
        for article in articles:
            custom_article_widget = ArticlesListWidgetItem(article)
            list_widget_item = QListWidgetItem(self)
            list_widget_item.setSizeHint(custom_article_widget.sizeHint())
            self.addItem(list_widget_item)
            self.setItemWidget(list_widget_item,custom_article_widget)


class SourceTreeWidget(QTreeWidget):

    def __init__(self,feed_data):
        super().__init__()
        self.setColumnCount(1)
        self.rss_sources = self.generate_source_tree_data(feed_data)
        self.setHeaderLabels(["Catogery"])
        source_tree_items = self.construct_source_tree(self.rss_sources)
        print(len(source_tree_items))
        self.insertTopLevelItems(0,source_tree_items)
        self.itemClicked.connect(self.list_articles_of_source)


    source_selected = Signal(str,str)

    def generate_source_tree_data(self,feed_data):
        source_tree_data = dict()
        for category in feed_data.keys():
            source_tree_data[category] = list(feed_data[category].keys())
        return source_tree_data

    @Slot(QTreeWidgetItem,int)
    def list_articles_of_source(self,item,column):
        item_category = item.parent().text(column)
        item_source = item.text(column)
        self.source_selected.emit(item_category,item_source)

    def construct_source_tree(self,rss_sources):
        items = []
        for category,sources in rss_sources.items():
            source_category = QTreeWidgetItem([category])
            print(category,sources)
            for source in sources:
                source_name = QTreeWidgetItem([source])
                source_category.addChild(source_name)
            items.append(source_category)
        return items


