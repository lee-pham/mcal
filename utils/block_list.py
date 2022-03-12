class BlockList:
    def __init__(self, num_elements):
        self.block_list = [None] * num_elements

    def hold_index(self, i, e):
        self.block_list[i] = e
        return self.block_list

    def fill(self, e):
        for idx in range(len(self.block_list)):
            if self.block_list[idx] is None:
                self.block_list[idx] = e
                return self.block_list

    def to_list(self):
        return self.block_list


class TestBlockList:
    def test_initial_block_list_is_all_empty(self):
        assert BlockList(3).to_list() == [None, None, None]

    def test_fill_empty_block_list(self):
        bl = BlockList(3)
        bl.fill(1)
        bl.fill(2)
        bl.fill(3)
        assert bl.to_list() == [1, 2, 3]

    def test_hold_index_and_fill(self):
        bl = BlockList(3)
        bl.hold_index(1, 99)
        bl.fill(1)
        bl.fill(1)
        assert bl.to_list() == [1, 99, 1]
