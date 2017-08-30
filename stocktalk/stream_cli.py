import configargparse

def main():

    p = configargparse.ArgParser()
    p.add()

    options = p.parse_args()


if __name__ == "__main__":
    main()
