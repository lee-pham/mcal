class BlockList:
    def __init__(self, num_elements, none_element):
        self.none_element = none_element
        self.block_list = [none_element] * num_elements

    def hold_index(self, i, e):
        self.block_list[i] = e
        return self.block_list

    def fill(self, e):
        for idx in range(len(self.block_list)):
            if self.block_list[idx] is self.none_element:
                self.block_list[idx] = e
                return self.block_list

    def to_list(self):
        if not self.block_list:
            return self.block_list
        while self.block_list[-1] == self.none_element:
            self.block_list.pop()
        return self.block_list


class TestBlockList:
    def test_fill_empty_block_list(self):
        bl = BlockList(3, None)
        bl.fill(1)
        bl.fill(2)
        bl.fill(3)
        assert bl.to_list() == [1, 2, 3]

    def test_hold_index_and_fill(self):
        bl = BlockList(3, None)
        bl.hold_index(1, 99)
        bl.fill(1)
        bl.fill(1)
        assert bl.to_list() == [1, 99, 1]

    def test_trailing_none_element(self):
        bl = BlockList(6, None)
        bl.fill(3)
        bl.fill(2)
        bl.fill(1)
        assert bl.to_list() == [3, 2, 1]
