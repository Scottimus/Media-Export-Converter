import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stremio_to_trakt import parse_stremio_html, convert_to_trakt_format


class ConverterTests(unittest.TestCase):
    def test_movie_episode_and_invalid_link(self):
        html = ('<a class="meta-item-container" href="#/detail/movie/tt0000001" title="Sample Film"></a>'
                '<a class="meta-item-container" href="#/detail/series/tt0000002:2:3" title="Sample Show"></a>'
                '<a class="meta-item-container" href="invalid">Unknown</a>')
        items = convert_to_trakt_format(parse_stremio_html(html), add_watchlist=False)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[1]["type"], "episode")
        self.assertEqual((items[1]["season"], items[1]["episode"]), (2, 3))

    def test_camel_case_progress_is_read(self):
        html = ('<a class="meta-item-container" href="#/detail/movie/tt0000001">'
                '<div class="progressBar" style="width:95%"></div></a>')
        self.assertEqual(parse_stremio_html(html)[0]["progress"], 95)

    def test_cli_empty_input_fails_and_valid_input_is_json(self):
        command = [sys.executable, str(ROOT / "stremio_to_trakt.py"), "--no-watchlist"]
        empty = subprocess.run(command, input="", text=True, capture_output=True)
        self.assertNotEqual(empty.returncode, 0)
        valid = subprocess.run(command + [str(ROOT / "examples/library.html")],
                               text=True, capture_output=True, check=True)
        self.assertEqual(len(json.loads(valid.stdout)), 2)

    def test_malformed_optional_attributes_are_ignored(self):
        html = ('<a class="meta-item-container" href="#/detail/movie/tt0000001">'
                '<div class="progressBar" style="width:..%"></div><div class></div></a>')
        self.assertEqual(len(parse_stremio_html(html)), 1)

    def test_cli_preserves_input_and_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "library.html"
            source.write_text('<a class="meta-item-container" href="#/detail/movie/tt0000001"></a>')
            original = source.read_bytes()
            command = [sys.executable, str(ROOT / "stremio_to_trakt.py"), str(source), "-o", str(source)]
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
