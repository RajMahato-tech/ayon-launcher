import signal
from qtpy import QtWidgets, QtCore, QtGui

from ayon_common.resources import (
    get_icon_path,
    load_stylesheet,
)
from ayon_common.ui_utils import get_qt_app


class AnimationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        legs_start_anim = QtCore.QVariantAnimation()
        legs_start_anim.setStartValue(0.0)
        legs_start_anim.setEndValue(1.0)
        legs_start_anim.setDuration(1000)
        legs_start_anim.setEasingCurve(QtCore.QEasingCurve.InQuart)

        legs_mid_anim = QtCore.QVariantAnimation()
        legs_mid_anim.setStartValue(0.0)
        legs_mid_anim.setEndValue(4.0)
        legs_mid_anim.setDuration(1000)

        legs_end_anim = QtCore.QVariantAnimation()
        legs_end_anim.setStartValue(1.0)
        legs_end_anim.setEndValue(0.0)
        legs_end_anim.setDuration(2000)
        legs_end_anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)

        legs_anim_group = QtCore.QSequentialAnimationGroup()
        legs_anim_group.addPause(300)
        legs_anim_group.addAnimation(legs_start_anim)
        legs_anim_group.addAnimation(legs_mid_anim)
        legs_anim_group.addAnimation(legs_end_anim)

        # Ball animation
        ball_start_anim = QtCore.QVariantAnimation()
        ball_start_anim.setStartValue(1.0)
        ball_start_anim.setEndValue(0.0)
        ball_start_anim.setDuration(300)
        ball_start_anim.setEasingCurve(QtCore.QEasingCurve.InBack)

        ball_end_anim = QtCore.QVariantAnimation()
        ball_end_anim.setStartValue(ball_start_anim.endValue())
        ball_end_anim.setEndValue(ball_start_anim.startValue())
        ball_end_anim.setDuration(300)
        ball_end_anim.setEasingCurve(QtCore.QEasingCurve.OutBack)

        ball_anim_group = QtCore.QSequentialAnimationGroup()
        ball_anim_group.addPause(300)
        ball_anim_group.addAnimation(ball_start_anim)
        ball_anim_group.addPause(
            (
                legs_start_anim.duration()
                + legs_mid_anim.duration()
                + (legs_end_anim.duration() * 0.5)
            )
            - ball_anim_group.duration()
        )
        ball_anim_group.addAnimation(ball_end_anim)
        ball_anim_group.addPause(
            legs_anim_group.duration() - ball_anim_group.duration()
        )

        anim_group = QtCore.QParallelAnimationGroup()
        anim_group.addAnimation(legs_anim_group)
        anim_group.addAnimation(ball_anim_group)

        repaint_timer = QtCore.QTimer()
        repaint_timer.setInterval(10)

        legs_start_anim.valueChanged.connect(self._on_legs_anim_value_change)
        legs_end_anim.valueChanged.connect(self._on_legs_anim_value_change)
        legs_mid_anim.valueChanged.connect(self._on_legs_mid_valud_change)
        ball_start_anim.valueChanged.connect(self._on_ball_anim_value_change)
        ball_end_anim.valueChanged.connect(self._on_ball_anim_value_change)
        repaint_timer.timeout.connect(self.repaint)

        anim_group.finished.connect(self._on_anim_group_finish)

        self._ball_offset_ratio = ball_start_anim.startValue()
        self._legs_angle = 0
        self._anim_group = anim_group
        self._repaint_timer = repaint_timer

    def _on_legs_anim_value_change(self, value):
        self._legs_angle = int(value * 360)

    def _on_legs_mid_valud_change(self, value):
        self._legs_angle = int(360 * value) % 360

    def _on_ball_anim_value_change(self, value):
        self._ball_offset_ratio = value

    def _on_anim_group_finish(self):
        self._anim_group.start()

    def showEvent(self, event):
        super().showEvent(event)
        self._anim_group.start()
        self._repaint_timer.start()

    def sizeHint(self):
        height = self.fontMetrics().height()
        return QtCore.QSize(height, height)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        render_hints = (
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )
        if hasattr(QtGui.QPainter, "HighQualityAntialiasing"):
            render_hints |= QtGui.QPainter.HighQualityAntialiasing
        event_rect = event.rect()
        event_width = event_rect.width()
        event_height = event_rect.height()
        base_size = min(event_width, event_height)

        ball_offset = base_size * 0.1
        legs_content_size = base_size - ball_offset

        legs_content_half = legs_content_size * 0.5
        leg_rect_width = int(legs_content_half * 0.7)
        leg_rect_height = int(legs_content_half * 0.2)
        leg_center_offset = int(legs_content_half * 0.2)
        leg_border_offset = legs_content_half - (
            leg_rect_width + leg_center_offset
        )

        ball_size = ball_offset + leg_border_offset

        ball_top_offset = (
            ((leg_border_offset * 2) + ball_offset)
            * self._ball_offset_ratio
        )
        ball_rect = QtCore.QRect(
            (event_width * 0.5) - (ball_size * 0.5),
            (event_height - base_size) + ball_top_offset,
            ball_size,
            ball_size
        )

        leg_rect = QtCore.QRect(
            leg_center_offset, -leg_rect_height * 0.5,
            leg_rect_width, leg_rect_height
        )

        painter.setRenderHints(render_hints)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 215, 160))

        painter.drawEllipse(ball_rect)
        painter.translate(
            event_width * 0.5,
            (event_height * 0.5) + (ball_size * 0.5)
        )
        painter.rotate(self._legs_angle + 90)
        painter.drawRect(leg_rect)
        painter.rotate(120)
        painter.drawRect(leg_rect)
        painter.rotate(120)
        painter.drawRect(leg_rect)

        painter.end()


class UpdateMessageWidget(QtWidgets.QWidget):
    def __init__(self, message, parent):
        super().__init__(parent)

        self._message = message
        self.setStyleSheet("font-size: 36pt;")

    def sizeHint(self):
        fm = self.fontMetrics()
        rect = fm.boundingRect(self._message)
        size = rect.size()
        padding = fm.height() * 0.2
        return QtCore.QSize(
            size.width() + (padding * 2),
            size.height() + (padding * 2)
        )

    def showEvent(self, event):
        super().showEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        render_hints = (
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )
        if hasattr(QtGui.QPainter, "HighQualityAntialiasing"):
            render_hints |= QtGui.QPainter.HighQualityAntialiasing

        event_rect = event.rect()
        fm = self.fontMetrics()
        padding = fm.height() * 0.2
        b_rect = fm.boundingRect(self._message)
        bg_pos_x = (
            (event_rect.width() * 0.5)
            - ((b_rect.width() * 0.5) + padding)
        )

        text_rect = QtCore.QRect(
            bg_pos_x + padding,
            event_rect.y() + padding,
            b_rect.width(),
            b_rect.height()
        )
        pen_width = text_rect.height() * 0.05
        if pen_width < 1:
            pen_width = 1
        bg_rect = QtCore.QRect(
            bg_pos_x + pen_width,
            event_rect.y() + pen_width,
            b_rect.width() + (padding * 2) - (pen_width * 2),
            (b_rect.height() + (padding * 2)) - (pen_width * 2)
        )
        radius = bg_rect.height() * 0.3

        painter.setRenderHints(render_hints)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("#D3D8DE"))
        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor("#2C313A"))
        painter.drawRoundedRect(bg_rect, radius, radius)
        painter.drawText(text_rect, self._message)

        painter.end()


class UpdateWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Set icon and title for task icon
        icon_path = get_icon_path()
        icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle("AYON Update...")

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.CustomizeWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        message_label = UpdateMessageWidget("Updating...", self)

        anim_widget = AnimationWidget(self)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(anim_widget, 1)
        main_layout.addWidget(message_label, 0)

    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet(load_stylesheet())
        self.resize(500, 500)


if __name__ == "__main__":
    app = get_qt_app()
    window = UpdateWindow()
    window.show()

    def signal_handler(*_args):
        window.close()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app.exec_()
