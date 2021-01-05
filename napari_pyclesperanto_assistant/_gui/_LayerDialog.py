from qtpy import QtGui
from qtpy.QtWidgets import QLabel
from magicgui._qt.widgets import QDataComboBox


class LayerDialog():
    """
    The LayerDialog contains a dock-widget that allows configuring parameters of all _operations.
    It uses events emitted by napari to toggle which dock widget is shown.
    """
    def __init__(self, viewer, operation):
        self.viewer = viewer

        self.operation = operation
        self.operation.self = self # arrrrg

        former_active_layer = self.viewer.active_layer
        try:
            former_active_layer.metadata['dialog']._deselected(None)
        except AttributeError:
            pass
        except KeyError:
            pass

        self.operation.initial_call = True
        self.operation(self.viewer.active_layer)
        self.layer = self.viewer.active_layer
        if(self.layer is None):
            import time
            self.operation(self.viewer.active_layer)
            time.sleep(0.1) # dirty workaround: wait until napari has set its active_layer
            self.layer = self.viewer.active_layer

        self.layer.metadata['dialog'] = self

        self.layer.events.data.connect(self._updated)
        self.layer.events.select.connect(self._selected)
        self.layer.events.deselect.connect(self._deselected)

        self.filter_gui = self.operation.Gui()
        self.dock_widget = viewer.window.add_dock_widget(self.filter_gui, area='right')
        self.dock_widget.setMaximumWidth(300)
        try:
            if self.filter_gui.get_widget('input1') is not None:
                self.filter_gui.set_widget('input1', former_active_layer)
        except AttributeError:
            pass

        for i in reversed(range(self.filter_gui.layout().count())):
            widget = self.filter_gui.layout().itemAt(i).widget()
            widget.setFont(QtGui.QFont('Arial', 12))
            if isinstance(widget, QDataComboBox):
                widget.setMaximumWidth(200)
            if isinstance(widget, QLabel):
                widget.setMaximumWidth(100)

    def _updated(self, event):
        self.refresh_all_followers()

    def _selected(self, event):
        self.operation.self = self    # sigh
        self.dock_widget = self.viewer.window.add_dock_widget(self.filter_gui, area='right')

    def _deselected(self, event):
        if hasattr(self, 'dock_widget'):
            self.viewer.window.remove_dock_widget(self.dock_widget)

    def _removed(self):
        if hasattr(self, 'dock_widget'):
            self.viewer.window.remove_dock_widget(self.dock_widget)

    def refresh(self):
        """
        Refresh/recompute the current layer
        """
        former = self.operation.self
        self.operation.self = self    # sigh
        self.filter_gui()
        self.operation.self = former

    def refresh_all_followers(self):
        """
        Go through all layers and identify layers which have the current layer (self.layer) as parameter.
        Then, refresh those layers.
        """
        for layer in self.viewer.layers:
            if layer != self.layer:
                try:
                    if layer.metadata['dialog'].filter_gui.get_widget('input1').currentData() == self.layer:
                        print(self.layer.name + " refreshes " + layer.name)
                        layer.metadata['dialog'].refresh()
                    if layer.metadata['dialog'].filter_gui.get_widget('input2').currentData() == self.layer:
                        layer.metadata['dialog'].refresh()
                except AttributeError:
                    pass
                except KeyError:
                    pass
