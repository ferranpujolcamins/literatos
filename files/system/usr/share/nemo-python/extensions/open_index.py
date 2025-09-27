#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Nemo extension to auto-open index.html on folder change,
# closing the previous one.

from gi.repository import Nemo, GObject
import os
import subprocess

class OpenIndexExtension(GObject.GObject, Nemo.LocationWidgetProvider):
    """
    Implements Nemo.LocationWidgetProvider so that get_widget()
    is called on every directory change.
    We don’t actually add any UI widget—returning None—but
    use the hook to launch/kill our browser process.
    """

    def __init__(self):
        super().__init__()
        # store the last browser subprocess.Popen object
        self.browser_proc = None

    def get_widget(self, uri, window):
        """
        Called by Nemo whenever the location (uri) changes.
        uri: a GFile representing the new location.
        window: the Gtk.Window instance (unused here).
        """
        # Convert the GFile URI to a filesystem path
        path = uri.get_path()
        if not path:
            return None

        index_path = os.path.join(path, "index.html")

        # 1) Kill any previously opened browser
        if self.browser_proc:
            try:
                self.browser_proc.terminate()
            except Exception:
                pass
            self.browser_proc = None

        # 2) If index.html exists in the new folder, open it
        if os.path.isfile(index_path):
            # xdg-open will use your default browser
            self.browser_proc = subprocess.Popen(["xdg-open", index_path])

        # We don’t need to add any widget to Nemo’s UI
        return None
