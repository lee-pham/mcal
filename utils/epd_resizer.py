from PIL import Image


def process_for_epd(img: Image.Image) -> Image.Image:
    return img.resize((768, 960))


class TestProcessForEPD:
    test_image = Image.open("test_image.png")
    
    def test_returns_Image(self) -> None:
        assert isinstance(process_for_epd(self.test_image), Image.Image)

    def test_returns_768x960_resolution(self) -> None:
        assert process_for_epd(self.test_image).size == (768, 960)
