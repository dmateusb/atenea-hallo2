
import sys
import unittest
from pathlib import Path

# Add python directory to path
sys.path.append(str(Path(__file__).parent.parent / 'python'))

from config_generator import get_quality_preset

class TestQualityPresets(unittest.TestCase):
    def test_balanced_preset(self):
        preset = get_quality_preset('balanced')
        self.assertEqual(preset['resolution'], 512)
        self.assertEqual(preset['steps'], 40)
        self.assertEqual(preset['lip_weight'], 1.0)
        self.assertEqual(preset['cfg_scale'], 3.5)

    def test_high_preset(self):
        preset = get_quality_preset('high')
        self.assertEqual(preset['resolution'], 768)
        self.assertEqual(preset['steps'], 50)
        self.assertEqual(preset['lip_weight'], 1.1)
        self.assertEqual(preset['cfg_scale'], 3.8)

    def test_ultra_preset(self):
        preset = get_quality_preset('ultra')
        self.assertEqual(preset['resolution'], 768)
        self.assertEqual(preset['steps'], 60)
        self.assertEqual(preset['lip_weight'], 1.0)
        self.assertEqual(preset['cfg_scale'], 4.5)

if __name__ == '__main__':
    unittest.main()
