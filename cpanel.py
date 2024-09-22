import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=None)

    parser.add_argument('-m', '--mode', default=None, type=str, help=None)

    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary

    if args.mode == 'update_opt':
        # python -m cpanel --mode update_opt
        from src.pages import update_opt
        update_opt()