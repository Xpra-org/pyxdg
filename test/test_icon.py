#!/usr/bin/env python3
from xdg import IconTheme as IconThemeModule
from xdg.IconTheme import IconTheme, getIconPath, getIconData, clear_cache
import tempfile, shutil, os
import unittest

import resources

example_dir = os.path.join(os.path.dirname(__file__), 'example')
def example_file(filename):
    return os.path.join(example_dir, filename)

class IconThemeTest(unittest.TestCase):
    def test_find_icon_exists(self):
        print("Finding an icon that probably exists:")
        print (getIconPath("firefox"))

    def test_find_icon_nonexistant(self):
        icon = getIconPath("oijeorjewrjkngjhbqefew")
        assert icon is None, "%r is not None" % icon
    
    def test_validate_icon_theme(self):
        theme = IconTheme()
        theme.parse(example_file("index.theme"))
        theme.validate()

    def test_clear_cache(self):
        getIconPath("oijeorjewrjkngjhbqefew")
        assert IconThemeModule.dir_cache or IconThemeModule.icon_cache or not IconThemeModule.icondirs
        clear_cache()
        assert IconThemeModule.themes == []
        assert IconThemeModule.theme_cache == {}
        assert IconThemeModule.dir_cache == {}
        assert IconThemeModule.icon_cache == {}

class IconDataTest(unittest.TestCase):
    def test_read_icon_data(self):
        tmpdir = tempfile.mkdtemp()
        try:
            png_file = os.path.join(tmpdir, "test.png")
            with open(png_file, "wb") as f:
                f.write(resources.png_data)
            
            icon_file = os.path.join(tmpdir, "test.icon")
            with open(icon_file, "w") as f:
                f.write(resources.icon_data)
            
            icondata = getIconData(png_file)
            icondata.validate()
            
            self.assertEqual(icondata.getDisplayName(), 'Mime text/plain')
            self.assertEqual(icondata.getAttachPoints(), [(200,200), (800,200), (500,500), (200,800), (800,800)])
            self.assertEqual(icondata.getEmbeddedTextRectangle(), [100,100,900,900])
            
            assert "<IconData" in repr(icondata), repr(icondata)
        
        finally:
            shutil.rmtree(tmpdir)
        
