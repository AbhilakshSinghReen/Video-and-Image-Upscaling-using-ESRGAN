import numpy as np

def combine_blocks_into_image(blocks_data):
    rows, cols = blocks_data[0]
    blocks = blocks_data[1]

    channels = blocks[0].shape[2]

    height, width, channels = 0, 0, 0

    currentCol, currentRow = 0, 0

    for block in blocks:
        currentCol += 1
        width += block.shape[1]

        if (currentCol > cols):
            currentCol = 0
            currentRow += 1

            height += block.shape[0]

            if not currentRow > rows:
                width = 0

    # FIX THIS
    channels = 3

    image = np.zeros((height, width, channels), dtype=np.float32)

    i = 0
    j = 0
    for image_cell in blocks:
        image_cell_height, image_cell_width, image_cell_channels = image_cell.shape

        image[j:j + image_cell_height, i:i+image_cell_width] = image_cell
                
        i += image_cell_width
        if (i >= width):
            i = 0
            j += image_cell_height
                
        if (j >= height):
            break
            
    return image