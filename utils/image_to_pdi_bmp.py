from PIL import Image

w = 960
h = 768


def convert_image_to_epd_bytes(image_name: str, former_name: str, latter_name: str) -> None:
    with Image.open(image_name) as im:
        im.thumbnail((w, h))
        former = im.crop((0, 0, w // 2, h)).convert(mode="1")
        former.show()
        latter = im.crop((w // 2, 0, w, h)).convert(mode="1")
        latter.show()

        names = [former_name, latter_name]
        for idx, display in enumerate([former, latter]):
            pixels = ["0" if e == 255 else "1" for e in list(display.getdata())]
            out = []
            for i in range(0, len(pixels), w // 2):
                hex_code = hex(int("".join(pixels)[i:i + (w // 2)], 2))[2:]
                n = 2
                line = hex_code
                a = "".join([f"0x{line[i:i + n]}, " for i in range(0, len(line), n)]) + "\n"
                out.append(a)

            file_name = names[idx]
            with open(f"{file_name}.c", "w") as f:
                f.write(f"const uint8_t {file_name}[]={{" + "\n")
                f.writelines(out)
                f.write("};")


convert_image_to_epd_bytes("peppos.png", "Image_970_Masterfm_01", "Image_970_Slavefm_01")
