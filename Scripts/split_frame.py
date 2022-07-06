def split_image_into_blocks(image, block_size):
    height, width, channels = image.shape

    max_x_size = 300
    max_y_size = 300

    rows = int(height / max_y_size) + 1
    cols = int(width / max_x_size) + 1

    blocks = []

    for r in range (0, rows):
        for c in range(0, cols):
            y_start = r * max_y_size
            y_end = (r + 1) * max_y_size
            x_start = c * max_x_size
            x_end = (c + 1) * max_x_size

            if (x_end < width and y_end < height):
                image_rc = image[y_start:y_end, x_start:x_end]
                        # print("ok")
            elif (x_end >= width and y_end < height):
                        # print("x not ok")
                image_rc = image[y_start:y_end, x_start:(width - 1)]
            elif (x_end < width and y_end >= height):
                        # print("y not ok")
                image_rc = image[y_start:(height - 1), x_start:x_end]
            else:
                        # print("both not ok")
                image_rc = image[y_start:(height - 1), x_start:(width - 1)]

            # print(image_rc.shape)
            blocks.append(image_rc)

    return ((r, c), blocks)
    
