import time


class StopWatch:
    def __init__(self, name="", parent=None, handler=None):
        self.name = name
        self.count = 0
        self.total_time = 0
        self.start_time = 0
        self.started = False
        self.parent = parent
        self.handler = handler

        self.children = []

    def start(self):
        self.started = True
        self.start_time = time.time()

    def stop(self):
        if self.started:
            self.total_time += time.time() - self.start_time
            self.count += 1
            self.started = False

    def mean_iteration_time(self):
        if self.count == 0:
            return float('Nan')
        return self.total_time / self.count

    def add_child(self, child):
        self.children.append(child)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if self.handler is not None:
            self.handler.current_stopwatch = self.parent

    def to_str(self, indent=1):
        my_repr = "%s: Total time %f, Iterations %d, %f iterations/sec" % (self.name, self.total_time, self.count, (self.count/self.total_time))
        return "\n".join(["\t"*indent+my_repr] + [c.to_str(indent+1) for c in self.children])

    def __repr__(self):
        return self.name


class StopwatchHandler:
    def __init__(self):
        self.current_stopwatch = None
        self.stopwatches = dict()

    def get(self, name):
        if name not in self.stopwatches:
            sw = StopWatch(name, self.current_stopwatch, self)
            self.stopwatches[name] = sw

            if self.current_stopwatch is not None:
                self.current_stopwatch.add_child(sw)

            self.current_stopwatch = sw

        return self.stopwatches[name]

    def print_recap(self):
        print("Stopwatches recap:")
        names = list(self.stopwatches.keys())
        names.sort()
        for s in names:
            if self.stopwatches[s].parent is None:
                print(self.stopwatches[s].to_str())


stopwatch = StopwatchHandler()
