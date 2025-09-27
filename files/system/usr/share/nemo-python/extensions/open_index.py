#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Nemo, GObject, Gio
import os
import subprocess
import shutil

class OpenIndexExtension2(GObject.GObject, Nemo.LocationWidgetProvider):
    """
    Open index.html for the current folder (if present) using luakit.
    Closes the previous luakit instance when the folder changes.
    """

    def __init__(self):
        super().__init__()
        self.browser_proc = None
        # Locate luakit binary
        self.luakit_bin = shutil.which("luakit")

    def get_widget(self, uri, window):
        # Handle only file:// URIs
        if not isinstance(uri, str) or not uri.startswith("file://"):
            return None

        gfile = Gio.File.new_for_uri(uri)
        folder_path = gfile.get_path()
        if not folder_path:
            return None

        index_path = os.path.join(folder_path, "index.html")
        if not os.path.isfile(index_path):
            # No index.html here → close previous if still running
            if self.browser_proc and self.browser_proc.poll() is None:
                try:
                    self.browser_proc.terminate()
                except Exception:
                    pass
                self.browser_proc = None
            return None

        index_uri = Gio.File.new_for_path(index_path).get_uri()

        # Kill any previously running luakit
        if self.browser_proc and self.browser_proc.poll() is None:
            try:
                self.browser_proc.terminate()
            except Exception:
                pass
            self.browser_proc = None

        # Start luakit if available
        if self.luakit_bin:
            try:
                self.browser_proc = subprocess.Popen([self.luakit_bin, index_uri])
            except Exception:
                pass

        return None

