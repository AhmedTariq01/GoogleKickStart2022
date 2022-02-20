def solve(board, n):
    num_red, num_blue = count_stones(board)
    if abs(num_red - num_blue) > 1:
        return "impossible"

    padded_board = pad_board(board, n)
    m = n + 2

    south_path = blue_path_south(padded_board, m)
    if south_path:
        north_path = blue_path_north(padded_board, m)
        common_blue_stones = south_path.intersection(north_path)
        if common_blue_stones and num_blue >= num_red:
            return "Blue wins"
        else:
            return "impossible"

    west_path = red_path(padded_board, m)
    if west_path:
        east_path = red_path_east(padded_board, m)
        common_red_stones = west_path.intersection(east_path)
        if common_red_stones and num_red >= num_blue:
            return "Red wins"
        else:
            return "impossible"

    return "Nobody wins"
