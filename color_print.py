
import random


class color_print:
    """ this module is just for fun """

    def __init__(self):
        """
        table of formatted text format options
        """
        self.colors = {}
        index = 0
        # for style in range(8):
        for fg in range(30, 38):
                # for bg in range(40, 48):
            fmt = ';'.join([str(1), str(fg), str(40)])
            self.colors[index] = '\x1b[%sm' % (fmt)
            index += 1
        self.options = index

    def color_print(self, output):
        index = random.randrange(self.options)
        print(self.colors[index] + output + '\x1b[0m')
