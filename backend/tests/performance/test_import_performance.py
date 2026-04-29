"""Performance regression tests."""

import importlib


class TestImportPerformance:
    def test_settings_import_fast(self, benchmark):
        """Settings module should import within a reasonable time."""

        def import_settings():

            importlib.reload(voice.config.settings)

        benchmark(import_settings)

    def test_enums_import_fast(self, benchmark):
        """Enums module should import within a reasonable time."""

        def import_enums():

            importlib.reload(voice.core.enums)

        benchmark(import_enums)
