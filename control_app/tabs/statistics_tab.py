from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QGridLayout, QFormLayout, \
    QLineEdit
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter
import json
from utils.saving_loading_json import load_setting_json, save_setting_json
from PyQt5.QtCore import Qt


class StatisticsTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot
        self.statistics_cog = bot.get_cog("Statistics")

        # buttons
        load_user_report_button = QPushButton("Load User Report")
        load_user_report_button.clicked.connect(self.load_user_report)

        load_channel_report_button = QPushButton("Load Channel Report")
        load_channel_report_button.clicked.connect(self.load_channel_report)

        generate_report_button = QPushButton("Generate Report")
        generate_report_button.clicked.connect(self.generate_report)

        # layout
        self.main_layout = QVBoxLayout()

        # upper part for the chart
        self.chart_layout = QVBoxLayout()

        # lower part for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(load_user_report_button)
        self.button_layout.addWidget(generate_report_button)
        self.button_layout.addWidget(load_channel_report_button)

        self.main_layout.addLayout(self.chart_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        # load the user report at the start
        self.load_channel_report()

    def generate_report(self):
        if self.statistics_cog:
            try:
                self.bot.loop.create_task(self.statistics_cog.collect_data())
            except Exception as e:
                print(f"Error collecting data: {e}")

    def load_user_report(self):
        user_data = load_setting_json("user_data")
        self.display_bar_chart(user_data, "User Activity", "User ID", "Messages Count")

    def load_channel_report(self):
        channel_stats = load_setting_json("channel_stats")
        self.display_bar_chart(channel_stats, "Channel Activity", "Channel ID", "Messages Count")

    def display_bar_chart(self, data, title, x_axis, y_axis):
        series = QBarSeries()
        categories = []
        bar_set = QBarSet(title)

        # sort data by message count
        sorted_data = sorted(data.items(), key=lambda item: item[1]["messages_count"], reverse=True)

        for key, value in sorted_data:
            categories.append(str(key))
            bar_set.append(value["messages_count"])

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # remove old chart if any
        if self.chart_layout.count() > 0:
            old_chart = self.chart_layout.itemAt(0).widget()
            self.chart_layout.removeWidget(old_chart)
            old_chart.deleteLater()

        self.chart_layout.addWidget(chart_view)
