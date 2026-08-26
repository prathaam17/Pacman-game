import os
from settings import MAP as DEFAULT_MAP

class MapLoader:
    @staticmethod
    def load_map(file_path):
        if not os.path.exists(file_path):
            return DEFAULT_MAP
        
        grid = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if line:
                    grid.append(list(line))
        return grid if grid else DEFAULT_MAP
