#!/usr/bin/env python3
from xdg import IconTheme as IconThemeModule
from xdg.IconTheme import (IconTheme, getIconPath, getIconData, clear_cache,
                           DirectoryMatchesSize, DirectorySizeDistance, LookupIcon)
from unittest import mock
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

class ScalableDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.themedir = os.path.join(self.tmpdir, "scalabletest")
        os.mkdir(self.themedir)
        theme_file = os.path.join(self.themedir, "index.theme")
        with open(theme_file, "w") as f:
            f.write(resources.scalable_index_theme)
        self.theme = IconTheme()
        self.theme.parse(theme_file)
        clear_cache()

    def tearDown(self):
        clear_cache()
        shutil.rmtree(self.tmpdir)

    def test_scalable_matches_size(self):
        assert DirectoryMatchesSize("big", 16, self.theme)
        assert DirectoryMatchesSize("big", 100, self.theme)
        assert DirectoryMatchesSize("big", 256, self.theme)
        assert not DirectoryMatchesSize("big", 8, self.theme)
        assert not DirectoryMatchesSize("big", 512, self.theme)

    def test_scalable_size_distance(self):
        self.assertEqual(DirectorySizeDistance("big", 100, self.theme), 0)
        self.assertEqual(DirectorySizeDistance("big", 10, self.theme), 6)
        self.assertEqual(DirectorySizeDistance("big", 300, self.theme), 44)
        self.assertEqual(DirectorySizeDistance("small", 64, self.theme), 48)

    def _add_icon(self, subdir, name="test-icon.svg"):
        d = os.path.join(self.themedir, subdir)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name), "w").close()
        return os.path.join(d, name)

    def test_lookup_uses_scalable_exact_match(self):
        big = self._add_icon("big")
        self._add_icon("fixed48", "test-icon.png")
        with mock.patch.object(IconThemeModule, "icondirs", [self.tmpdir]):
            # 100 is only in range for "big"; the fixed 48 dir is not exact
            self.assertEqual(LookupIcon("test-icon", 100, self.theme, ["png", "svg"]), big)

    def test_lookup_closest_above_max_size(self):
        self._add_icon("small")
        big = self._add_icon("big")
        with mock.patch.object(IconThemeModule, "icondirs", [self.tmpdir]):
            # 512 is above both MaxSizes; "big" (256) is closer than "small" (16)
            self.assertEqual(LookupIcon("test-icon", 512, self.theme, ["svg"]), big)

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
        
