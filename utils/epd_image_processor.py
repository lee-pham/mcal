from PIL import Image, ImageOps


def convert_image_to_bytes(
        img: Image.Image,
        desired_resolution: tuple[int, int],
) -> bytes:
    resized_padded_bmp = img.convert("1", dither=Image.Dither.NONE)
    processed_image = ImageOps.mirror(ImageOps.invert(resized_padded_bmp))
    processed_image = processed_image.transpose(Image.TRANSPOSE)
    return processed_image.tobytes()

# class TestEPDImageProcessor:
    test_image = Image.open("test_image.png")
    test_width = 768
    test_height = 960
    test_num_subpanels = 2
    BITS_IN_A_BYTE = 8
    test_output = convert_image_to_list_of_bytes(test_image,
                                                 (test_width, test_height), test_num_subpanels)

    def test_returns_list_of_bytes(self):
        assert all([isinstance(e, bytes) for e in self.test_output])

    def test_returns_size_in_bytes(self):
        total_size = 0
        for image_data in self.test_output:
            total_size += len(image_data)
        assert total_size == self.test_width * self.test_height / self.BITS_IN_A_BYTE

    def test_returns_output_len_equal_to_num_subpanels(self):
        assert len(self.test_output) == self.test_num_subpanels


# convert_image_to_list_of_bytes(Image.open("../utils/test_image.png"), (768, 960), 2)
