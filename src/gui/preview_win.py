from PyQt5 import QtCore, QtGui, QtWidgets
import logging


class PreviewWindow(QtWidgets.QLabel):
    '''
        Paints the preview QLabel in MainWindow and maintains the aspect ratio
        when the window is resized.
    '''
    log = logging.getLogger('AVP.PreviewWindow')

    def __init__(self, parent, img):
        super(PreviewWindow, self).__init__()
        self.parent = parent
        self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0, 0)
        scaledPix = self.pixmap.scaled(
            size,
            QtCore.Qt.KeepAspectRatio,
            transformMode=QtCore.Qt.SmoothTransformation)

        # start painting the label from left upper corner
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        painter.drawPixmap(point, scaledPix)

    def changePixmap(self, img):
        self.pixmap = QtGui.QPixmap(img)
        self.repaint()

    def mousePressEvent(self, event):
        if self.parent.encoding:
            return

        i = self.parent.window.listWidget_componentList.currentRow()
        if i >= 0:
            component = self.parent.core.selectedComponents[i]
            if not hasattr(component, 'previewClickEvent'):
                self.log.info('Ignored click event')
                return
            pos = (event.x(), event.y())
            size = (self.width(), self.height())
            butt = event.button()
            self.log.info('Click event for #%s: %s button %s' % (
                i, pos, butt))
            component.previewClickEvent(
                pos, size, butt
            )
            self.parent.core.updateComponent(i)

    @QtCore.pyqtSlot(str)
    def threadError(self, msg):
        self.parent.showMessage(
            msg=msg,
            icon='Critical',
            parent=self
        )