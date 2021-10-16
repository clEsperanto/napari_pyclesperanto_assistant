from functools import partial
from ._categories import CATEGORIES
from ._gui._category_widget import make_gui_for_category
from napari_tools_menu import register_function, register_dock_widget

for name, category in CATEGORIES.items():
    register_dock_widget(partial(make_gui_for_category, category), menu = category.tools_menu + " > " + name + " (clEsperanto)")

