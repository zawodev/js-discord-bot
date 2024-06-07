from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFormLayout, QLineEdit
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter, QLinearGradient
import json
from utils.saving_loading_json import load_setting_json, save_setting_json
from PyQt5.QtCore import Qt, QPointF


class StatisticsTab(QWidget):
    """
    A QWidget subclass that provides an interface for viewing statistics related to user and channel activity.
    It displays bar charts for user and channel reports and provides buttons to load these reports.
    """

    def __init__(self, bot=None):
        """
        Initializes the StatisticsTab widget.

        :param bot: The bot instance, used to get the 'Statistics' cog.
        """
        super().__init__()
        self.bot = bot
        self.statistics_cog = bot.get_cog("Statistics")

        # Buttons
        load_user_report_button = QPushButton("Load User Report")
        load_user_report_button.clicked.connect(self.load_user_report)

        load_channel_report_button = QPushButton("Load Channel Report")
        load_channel_report_button.clicked.connect(self.load_channel_report)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.chart_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(load_user_report_button)
        self.button_layout.addWidget(load_channel_report_button)

        self.main_layout.addLayout(self.chart_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        # Load the channel report at the start
        self.load_channel_report()

    def load_user_report(self):
        """
        Loads user report data from JSON and displays it in a bar chart.
        """
        user_data = load_setting_json("user_data")
        self.display_bar_chart(user_data, "User Activity", "User Name", "Messages Count")

    def load_channel_report(self):
        """
        Loads channel report data from JSON and displays it in a bar chart.
        """
        channel_stats = load_setting_json("channel_stats")
        self.display_bar_chart(channel_stats, "Channel Activity", "Channel ID", "Messages Count")

    def display_bar_chart(self, data, title, x_axis, y_axis):
        """
        Displays a bar chart with the given data.

        :param data: Dictionary containing the data to be displayed.
        :param title: Title of the chart.
        :param x_axis: Label for the x-axis.
        :param y_axis: Label for the y-axis.
        """
        series = QBarSeries()
        categories = []
        bar_set = QBarSet(title)

        # Sort data by message count
        sorted_data = sorted(data.items(), key=lambda item: item[1]["messages_count"], reverse=True)

        for key, value in sorted_data:
            categories.append(value["name"])
            bar_set.append(value["messages_count"])

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setTitleText(x_axis)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText(y_axis)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        axisY.applyNiceNumbers()

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Remove old chart if any
        if self.chart_layout.count() > 0:
            old_chart = self.chart_layout.itemAt(0).widget()
            self.chart_layout.removeWidget(old_chart)
            old_chart.deleteLater()

        self.chart_layout.addWidget(chart_view)
