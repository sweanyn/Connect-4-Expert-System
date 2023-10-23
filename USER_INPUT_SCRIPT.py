# input_script.py

def main():
    move = input("Enter your move (column number): ")
    with open("temp_input.txt", "w") as file:
        file.write(move)

if __name__ == '__main__':
    main()

