class LayerDialog():
    """
    The LayerDialog contains a dock-widget that allows configuring parameters of all _operations.
    It uses events emitted by napari to toggle which dock widget is shown.
    """
    def __init__(self, viewer, stateful_function_factory):
        self.viewer = viewer
        self.stateful_function = stateful_function_factory.get()
        self.stateful_function.viewer = viewer

        self.filter_gui = self.stateful_function.get()
        self.filter_gui.native.setParent(viewer.window.qt_viewer)

        import warnings
        warnings.warn("are we leaking this?" + str(self.filter_gui.native))

        former_active_layer = self.viewer.active_layer
        try:
            former_active_layer.metadata['dialog']._deselected(None)
        except AttributeError:
            pass
        except KeyError:
            pass

        self.filter_gui(self.viewer.active_layer)
        self.layer = self.viewer.active_layer
        if self.stateful_function is not None:
            self.stateful_function.layer = self.layer

        if(self.layer is None):
            import time
            self.filter_gui(self.viewer.active_layer)
            time.sleep(0.1) # dirty workaround: wait until napari has set its active_layer
            self.layer = self.viewer.active_layer

        self.layer.metadata['dialog'] = self

        self.layer.events.data.connect(self._updated)
        self.layer.events.select.connect(self._selected)
        self.layer.events.deselect.connect(self._deselected)

        self.dock_widget = viewer.window.add_dock_widget(self.filter_gui, area='right')

        #self.dock_widget.setMaximumWidth(300)
        if hasattr(self.filter_gui, 'input1'):
            print("setting former active")
            self.filter_gui.input1.value = former_active_layer

        #for widget in self.filter_gui:
        #    widget.native.setFont(QtGui.QFont('Arial', 12))
        #    if isinstance(widget.native, ComboBox):
        #        widget.native.setMaximumWidth(200)
        #    if isinstance(widget.native, QLabel):
        #        widget.native.setMaximumWidth(100)

    def _updated(self, event):
        self.refresh_all_followers()

    def _selected(self, event):
        if hasattr(self, 'dock_widget'):
            self.dock_widget.show()
        else:
            self.dock_widget = self.viewer.window.add_dock_widget(self.filter_gui, area='right')

    def _deselected(self, event):
        if hasattr(self, 'dock_widget'):
            try:
                self.dock_widget.hide()
            except KeyError:
                pass

    def _removed(self):
        print("removed")
        if hasattr(self, 'dock_widget'):
            self.viewer.window.remove_dock_widget(self.dock_widget)

    def refresh(self):
        """
        Refresh/recompute the current layer
        """

        print("calling op")
        self.filter_gui()

    def refresh_all_followers(self):
        """
        Go through all layers and identify layers which have the current layer (self.layer) as parameter.
        Then, refresh those layers.
        """
        for layer in self.viewer.layers:
            if layer == self.layer:
                continue
            dialog = layer.metadata.get('dialog')
            if not dialog:
                continue
            gui = dialog.filter_gui

            if hasattr(gui, 'input1') and gui.input1.value == self.layer:
                dialog.refresh()
            if hasattr(gui, 'input2') and gui.input2.value == self.layer:
                dialog.refresh()

