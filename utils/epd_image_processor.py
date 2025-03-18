from PIL import Image, ImageOps


def convert_image_to_bytes(img: Image.Image, desired_resolution: tuple[int, int]) -> bytes:
    resized_padded_bmp = img.convert("1", dither=Image.Dither.NONE)
    processed_image = ImageOps.mirror(ImageOps.invert(resized_padded_bmp))
    processed_image = processed_image.transpose(Image.TRANSPOSE)
    return processed_image.tobytes()


# class TestEPDImageProcessor:
    test_image = Image.open("test_image.png")
    test_length = 768
    test_width = 960
    BITS_IN_A_BYTE = 8
    test_output = convert_image_to_bytes(test_image, (test_length, test_width))

    def test_returns_list_of_bytes(self):
        assert isinstance(self.test_output, bytes)

    def test_returns_size_in_bytes(self):
        total_size = self.test_length * self.test_width
        assert total_size == len(self.test_output) * self.BITS_IN_A_BYTE
