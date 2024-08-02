from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QPen, QBrush, QColor, QCursor
from PyQt6.QtCore import Qt, QRectF, QPointF
import sys

class ResizableRectItem(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(0, 0, w, h)
        self.setPos(x,y)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self.setBrush(QBrush(QColor(255, 255, 255, 100)))
        
        self.resizing = None
        self.edge_threshold = 10
        self.start_rect = None
        self.start_pos = None

    def hoverMoveEvent(self, event):
        if self.isSelected():
            pos = event.pos()
            print(f'{pos=}')
            cursor = self.get_resize_cursor(pos)
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)

    def get_resize_cursor(self, pos):
        rect = self.rect()
        if self.is_on_top_left(pos, rect) or self.is_on_bottom_right(pos, rect):
            return Qt.CursorShape.SizeFDiagCursor
        elif self.is_on_top_right(pos, rect) or self.is_on_bottom_left(pos, rect):
            return Qt.CursorShape.SizeBDiagCursor
        elif self.is_on_left_edge(pos, rect) or self.is_on_right_edge(pos, rect):
            return Qt.CursorShape.SizeHorCursor
        elif self.is_on_top_edge(pos, rect) or self.is_on_bottom_edge(pos, rect):
            return Qt.CursorShape.SizeVerCursor
        else:
            return Qt.CursorShape.ArrowCursor

    def is_on_left_edge(self, pos, rect):
        return abs(pos.x() - rect.left()) < self.edge_threshold

    def is_on_right_edge(self, pos, rect):
        return abs(pos.x() - rect.right()) < self.edge_threshold

    def is_on_top_edge(self, pos, rect):
        return abs(pos.y() - rect.top()) < self.edge_threshold

    def is_on_bottom_edge(self, pos, rect):
        return abs(pos.y() - rect.bottom()) < self.edge_threshold

    def is_on_top_left(self, pos, rect):
        return self.is_on_left_edge(pos, rect) and self.is_on_top_edge(pos, rect)

    def is_on_top_right(self, pos, rect):
        return self.is_on_right_edge(pos, rect) and self.is_on_top_edge(pos, rect)

    def is_on_bottom_left(self, pos, rect):
        return self.is_on_left_edge(pos, rect) and self.is_on_bottom_edge(pos, rect)

    def is_on_bottom_right(self, pos, rect):
        return self.is_on_right_edge(pos, rect) and self.is_on_bottom_edge(pos, rect)

    def mousePressEvent(self, event):
        if self.isSelected():
            pos = event.pos()
            rect = self.rect()
            self.start_rect = rect
            self.start_pos = pos
            self.resizing = self.get_resize_edge(pos, rect)
        if not self.resizing:
            super().mousePressEvent(event)

    def get_resize_edge(self, pos, rect):
        if self.is_on_top_left(pos, rect):
            return "top-left"
        elif self.is_on_top_right(pos, rect):
            return "top-right"
        elif self.is_on_bottom_left(pos, rect):
            return "bottom-left"
        elif self.is_on_bottom_right(pos, rect):
            return "bottom-right"
        elif self.is_on_left_edge(pos, rect):
            return "left"
        elif self.is_on_right_edge(pos, rect):
            return "right"
        elif self.is_on_top_edge(pos, rect):
            return "top"
        elif self.is_on_bottom_edge(pos, rect):
            return "bottom"
        return None


    def mouseMoveEvent(self, event):
        if self.resizing:
            new_pos = event.pos()
            dx = new_pos.x() - self.start_pos.x()
            dy = new_pos.y() - self.start_pos.y()
            new_rect = QRectF(self.start_rect)
            scene_rect = self.scene().sceneRect()
            item_scene_pos = self.scenePos()
            if self.resizing in ["left", "top-left", "bottom-left"]:
                left = new_rect.left() + dx
                real_coor = item_scene_pos.x() + left
                if real_coor < 0:
                    left = -item_scene_pos.x()
                new_rect.setLeft(left)
            if self.resizing in ["right", "top-right", "bottom-right"]:
                right = min(scene_rect.right(), max(new_rect.left(), item_scene_pos.x() + new_rect.right() + dx)) - item_scene_pos.x()
                new_rect.setRight(right)
            if self.resizing in ["top", "top-left", "top-right"]:
                top = new_rect.top() + dy
                new_rect.setTop(top)
            if self.resizing in ["bottom", "bottom-left", "bottom-right"]:
                bottom = min(scene_rect.bottom(), max(new_rect.top(), item_scene_pos.y() + new_rect.bottom() + dy)) - item_scene_pos.y()
                new_rect.setBottom(bottom)            
            self.setRect(new_rect)
        else:
            old_pos = self.pos()
            new_pos = old_pos + event.pos() - event.lastPos()
            rect = self.rect()
            scene_rect = self.scene().sceneRect()
            left_limit = scene_rect.left() - rect.left()
            right_limit = scene_rect.right() - rect.right()
            top_limit = scene_rect.top() - rect.top()
            bottom_limit = scene_rect.bottom() - rect.bottom()
            new_x = max(left_limit, min(new_pos.x(), right_limit))
            new_y = max(top_limit, min(new_pos.y(), bottom_limit))  
            self.setPos(QPointF(new_x, new_y))

    def mouseReleaseEvent(self, event):
        self.resizing = None
        self.start_rect = None
        self.start_pos = None
        super().mouseReleaseEvent(event)
