class LayerDialog:
    """
    The LayerDialog contains a dock-widget that allows configuring parameters of all
    _operations. It uses events emitted by napari to toggle which dock widget is shown.
    """

    def __init__(self, viewer, operation):
        self.viewer = viewer

        self.filter_gui = operation
        self.filter_gui._dialog = self  # arrrrg

        former_active_layer = self.viewer.active_layer
        try:
            former_active_layer.metadata["dialog"]._deselected(None)
        except AttributeError:
            pass
        except KeyError:
            pass

        self.filter_gui(self.viewer.active_layer)

        self.layer = self.viewer.active_layer
        if self.layer is None:
            from napari._qt import get_app

            get_app().processEvents()
            self.filter_gui(self.viewer.active_layer)
            self.layer = self.viewer.active_layer

        self.layer.metadata["dialog"] = self

        self.layer.events.data.connect(self.refresh_all_followers)
        self.layer.events.select.connect(self._selected)
        self.layer.events.deselect.connect(self._deselected)

        self.dock_widget = viewer.window.add_dock_widget(
            self.filter_gui, area="right", name=operation._function.__name__
        )
        self.filter_gui.native.setParent(self.dock_widget)

        if hasattr(self.filter_gui, "input1"):
            self.filter_gui.input1.value = former_active_layer

    def _selected(self, event):
        self.filter_gui._dialog = self  # sigh
        if hasattr(self, "dock_widget"):
            self.dock_widget.show()
        else:
            self.dock_widget = self.viewer.window.add_dock_widget(
                self.filter_gui, area="right"
            )

    def _deselected(self, event):
        if hasattr(self, "dock_widget"):
            try:
                self.dock_widget.hide()
            except KeyError:
                pass

    def _removed(self):
        if hasattr(self, "dock_widget"):
            self.viewer.window.remove_dock_widget(self.dock_widget)

    def refresh(self):
        """
        Refresh/recompute the current layer
        """
        former = self.filter_gui._dialog
        self.filter_gui._dialog = self  # sigh
        print("calling op")
        self.filter_gui()
        self.filter_gui._dialog = former

    def refresh_all_followers(self, *_):
        """
        Go through all layers and identify layers which have the current layer (self.layer) as parameter.
        Then, refresh those layers.
        """
        for layer in self.viewer.layers:
            if layer == self.layer:
                continue
            dialog = layer.metadata.get("dialog")
            if not dialog:
                continue
            gui = dialog.filter_gui

            if hasattr(gui, "input1") and gui.input1.value == self.layer:
                dialog.refresh()
            if hasattr(gui, "input2") and gui.input2.value == self.layer:
                dialog.refresh()
