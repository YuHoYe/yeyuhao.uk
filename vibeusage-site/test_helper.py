#!/usr/bin/env python3
"""Check Helper release links and installation instructions in temporary output.

No public pages or real downloads are modified. Fixture archives are plain test
bytes, created only inside a TemporaryDirectory and deleted when the test ends.
"""
import contextlib
from html.parser import HTMLParser
import io
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
import build


class Links(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.urls = []
        self.downloads = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("href", "src"):
            if attrs.get(name):
                self.urls.append(attrs[name])
        if tag == "a" and "download" in attrs:
            self.downloads.append(attrs["href"])


class HelperReleaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="vibeusage-site-test-")
        self.addCleanup(self.directory.cleanup)
        self.output = Path(self.directory.name) / "vibeusage"

    def render(self):
        with contextlib.redirect_stdout(io.StringIO()):
            build.build(self.output)

    def put_archive(self, name, data=b"TEST FIXTURE; not a distribution archive."):
        archive = self.output / "downloads" / name
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(data)
        return archive

    def helper_pages(self):
        return [self.output / "helper/index.html", self.output / "cn/helper/index.html"]

    def assert_local_links_exist(self):
        for page in self.output.rglob("index.html"):
            for url in Links(page.read_text()).urls:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = page.parent / parsed.path
                if target.is_dir():
                    target /= "index.html"
                self.assertTrue(target.is_file(), f"broken relative link: {page} -> {url}")

    def test_missing_release_has_no_download_link(self):
        self.render()
        for page in self.helper_pages():
            parser = Links(page.read_text())
            self.assertEqual(parser.downloads, [])
            self.assertIn('role="status"', page.read_text())
        self.assert_local_links_exist()

    def test_previous_release_does_not_make_current_release_available(self):
        old = self.put_archive("vibeUsage-Helper-1.0.0.zip")
        original = old.read_bytes()
        self.render()
        self.assertEqual(old.read_bytes(), original)
        for page in self.helper_pages():
            self.assertEqual(Links(page.read_text()).downloads, [])
        self.assert_local_links_exist()

    def test_current_downloads_resolve_and_all_archives_survive_rebuild(self):
        old = self.put_archive("vibeUsage-Helper-1.0.0.zip", b"previous release fixture")
        current = self.put_archive(build.HELPER_ARCHIVE)
        expected = {archive.name: archive.read_bytes() for archive in (old, current)}
        self.render()
        self.render()
        for page in self.helper_pages():
            downloads = Links(page.read_text()).downloads
            self.assertEqual(len(downloads), 1)
            self.assertEqual((page.parent / downloads[0]).resolve(), current.resolve())
            self.assertIn(build.HELPER_VERSION, page.read_text())
        actual = {archive.name: archive.read_bytes() for archive in current.parent.iterdir()}
        self.assertEqual(actual, expected)
        self.assert_local_links_exist()

    def test_empty_current_archive_is_not_offered(self):
        self.put_archive(build.HELPER_ARCHIVE, b"")
        self.render()
        for page in self.helper_pages():
            self.assertEqual(Links(page.read_text()).downloads, [])

    def test_language_switch_stays_on_helper_page(self):
        self.render()
        english, chinese = self.helper_pages()
        self.assertIn('../cn/helper/', Links(english.read_text()).urls)
        self.assertIn('../../helper/', Links(chinese.read_text()).urls)

    def test_both_entry_paths_and_system_confirmation_are_explained(self):
        self.render()
        english, chinese = (page.read_text() for page in self.helper_pages())
        self.assertIn("Your browser downloads the ZIP directly", english)
        self.assertIn("Setup started from vibeUsage connects automatically", english)
        self.assertIn("If you started from this page", english)
        self.assertIn("if macOS asks", english)
        self.assertIn("浏览器会直接下载 ZIP", chinese)
        self.assertIn("从 vibeUsage 发起的安装会自动连接", chinese)
        self.assertIn("从本页直接下载的用户", chinese)
        self.assertIn("如果 macOS 提示是否打开", chinese)


if __name__ == "__main__":
    unittest.main()
