import pygame, math

def blit_rotate(surf, image, pos, originPos, angle): ## https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame/54714144

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()),1)

    return rotated_image

def angle_of_vector(x, y): ## https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-points
    return pygame.math.Vector2(x, y).angle_to((1, 0))

def angle_of_line(x1, y1, x2, y2): ## ^
    return angle_of_vector(x2-x1, y2-y1)

def point_pos(x0, y0, d, theta): ## https://stackoverflow.com/questions/23280636/python-find-a-x-y-coordinate-for-a-given-point-b-using-the-distance-from-the-po
    theta_rad = math.pi/2 - math.radians(theta)
    return x0 + d*math.cos(theta_rad), y0 + d*math.sin(theta_rad)