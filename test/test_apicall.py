import unittest
import os
import json
from datetime import datetime
import sys

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)

from Dataset.coord_converter import convert_to_grid

class WeatherAPITest(unittest.TestCase):

    def test_danger_json_update(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, 'algorithms', 'danger.json')

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # danger.json에 '날씨' 필드가 생겼는지, 올바른 구조인지 확인
        for id, item in data.items():
            self.assertIn('날씨', item)
            날씨 = item['날씨']
            self.assertIsInstance(날씨, dict)

            # 각 시간대별 항목 확인
            for baseTime, categories in 날씨.items():
                self.assertIsInstance(categories, dict)
                # 원하는 카테고리들이 일부라도 들어있는지 확인
                self.assertTrue(
                    any(cat in categories for cat in ['T1H', 'PTY', 'SKY', 'REH', 'WSD']),
                    f"No weather categories found for {id} at {baseTime}"
                )