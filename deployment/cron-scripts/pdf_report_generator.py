# coding=utf-8

# A simple demonstration of how to load a QGIS project and then
# show it in a widget.
# This code is public domain, use if for any purpose you see fit.
# Tim Sutton 2015

import os
import sys
from qgis.core import (
    QgsProject, QgsComposition, QgsApplication)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument


gui_flag = True
app = QgsApplication(sys.argv, gui_flag)

# Make sure QGIS_PREFIX_PATH is set in your env if needed!
app.initQgis()
project_path = os.path.dirname(__file__) + os.path.sep + 'test.qgs'
template_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'test.qpt'
))


def make_pdf():
    global canvas, bridge, template_file, template_content, document, composition, substitution_map, map_item, legend_item
    canvas = QgsMapCanvas()
    # Load our project
    bridge = QgsLayerTreeMapCanvasBridge(
        QgsProject.instance().layerTreeRoot(), canvas)
    QgsProject.instance().read(QFileInfo(project_path))
    if canvas.layerCount() < 1:
        print 'No layers loaded from this project, exiting.'
        return
    print canvas.mapSettings().extent().toString()
    template_file = file(template_path)
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    composition = QgsComposition(canvas.mapSettings())
    # You can use this to replace any string like this [key]
    # in the template with a new value. e.g. to replace
    # [date] pass a map like this {'date': '1 Jan 2012'}
    substitution_map = {
        'DATE_TIME_START': 'foo',
        'DATE_TIME_END': 'bar'}
    composition.loadFromTemplate(document, substitution_map)
    # You must set the id in the template
    map_item = composition.getComposerItemById('map')
    map_item.setMapCanvas(canvas)
    map_item.zoomToExtent(canvas.extent())
    # You must set the id in the template
    legend_item = composition.getComposerItemById('legend')
    legend_item.updateLegend()
    composition.refreshItems()
    composition.exportAsPDF('/tmp/test2.pdf')
    QgsProject.instance().clear()


make_pdf()
make_pdf()


