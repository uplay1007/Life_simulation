from superqt import QLabeledSlider, QLabeledRangeSlider, QLabeledDoubleRangeSlider


class QLRSlider(
    QLabeledRangeSlider):  # создаем свой класс для слайдера, чтобы переопределить поведение слайдера для возможного спаривания бегунков
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._slider._neighbor_bound = self._neighbor_bound

    def _neighbor_bound(self, val, index):
        # make sure we don't go lower than any preceding index:
        min_dist = self.singleStep()
        _lst = self._position
        if index > 0:
            val = max(_lst[index - 1] + min_dist - 1, val)
        # make sure we don't go higher than any following index:
        if index < (len(_lst) - 1):
            val = min(_lst[index + 1] - min_dist + 1, val)
        return val


class QLDRSlider(
    QLabeledDoubleRangeSlider):  # создаем свой класс для слайдера, чтобы переопределить поведение слайдера для возможного спаривания бегунков
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._slider._neighbor_bound = self._neighbor_bound

    def _neighbor_bound(self, val, index):
        # make sure we don't go lower than any preceding index:
        min_dist = self.singleStep()
        _lst = self._position
        if index > 0:
            val = max(_lst[index - 1] + min_dist - 1, val)
        # make sure we don't go higher than any following index:
        if index < (len(_lst) - 1):
            val = min(_lst[index + 1] - min_dist + 1, val)
        return val
