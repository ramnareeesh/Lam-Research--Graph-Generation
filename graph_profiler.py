import time
import psutil
from memory_profiler import profile
import cProfile
import pstats
import io

class GraphProfiler:
    def __init__(self):
        self.process = psutil.Process()

    def measure_time(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Time taken by {func.__name__}: {end_time - start_time:.4f} seconds")
            return result
        return wrapper

    def measure_memory(self, func):
        @profile
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def detailed_profile(self, func):
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            result = profiler.runcall(func, *args, **kwargs)
            s = io.StringIO()
            ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
            ps.print_stats()
            print(s.getvalue())
            return result
        return wrapper

    def memory_usage(self):
        return self.process.memory_info().rss / 1024 / 1024  # in MB
