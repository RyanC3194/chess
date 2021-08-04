from PIL import Image

im = Image.open("chess_set.png")
w,h = im.size
w_sep = w / 6
h_sep = h / 2
im1 = im.crop((0,0, w_sep, h_sep))
im1.save("./b_king_image.png")
im1 = im.crop((w_sep,0, 2 * w_sep, h_sep))
im1.save("./b_queen_image.png")
im1 = im.crop((2 * w_sep,0, 3 * w_sep, h_sep))
im1.save("./b_rook_image.png")
im1 = im.crop((3 * w_sep,0, 4 * w_sep, h_sep))
im1.save("./b_bishop_image.png")
im1 = im.crop((4 * w_sep,0, 5 * w_sep, h_sep))
im1.save("./b_knight_image.png")
im1 = im.crop((5.3 * w_sep,0, 6 * w_sep, h_sep))
im1.save("./b_pawn_image.png")


im1 = im.crop((0,h_sep, w_sep, 2* h_sep))
im1.save("./w_king_image.png")
im1 = im.crop((w_sep,h_sep, 2 * w_sep, 2 * h_sep))
im1.save("./w_queen_image.png")
im1 = im.crop((2 * w_sep,h_sep, 3 * w_sep, 2 * h_sep))
im1.save("./w_rook_image.png")
im1 = im.crop((3 * w_sep,h_sep, 4 * w_sep, 2 * h_sep))
im1.save("./w_bishop_image.png")
im1 = im.crop((4 * w_sep,h_sep, 5 * w_sep, 2 * h_sep))
im1.save("./w_knight_image.png")
im1 = im.crop((5.3 * w_sep,h_sep, 6 * w_sep, 2 * h_sep))
im1.save("./w_pawn_image.png")