from Getch import _Getch

if __name__ == "__main__":
    print("Press a key")
    key_input = _Getch()
    while True:
        k = key_input()
        print("loop")
        print(f"You pressed {k}")
        if k == b'\x03':
            break



