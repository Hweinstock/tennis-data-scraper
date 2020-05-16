import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-y",
                        "--years",
                        metavar="",
                        choices=range(11),
                        default=1,
                        type=int,
                        help="argument describing how many years to go back, starting in 2019. Has default value of 1.")

    parser.add_argument("-p",
                        "--players",
                        metavar="",
                        choices=range(5000),
                        default=5,
                        type=int,
                        help="argument describing how many players' data to scrape. Has default value of 5.")

    parser.add_argument("-m",
                        "--mode",
                        metavar="",
                        choices=["marital_status", "basic-info"],
                        default="basic-info",
                        type=str,
                        help="argument describing what information the data collector should scrape in. Has default value of 'basic-info'.")

    parser.add_argument("-s",
                        "--singles",
                        metavar="",
                        choices=[True, False],
                        default=True,
                        type=bool,
                        help="argument describing whether it should look at top singles players or doubles players. Has default value of True")

    parser.add_argument("-d",
                        "--debug",
                        metavar="",
                        choices=[True, False],
                        default=False,
                        type=bool,
                        help="argument describing whether it should print debugging and progress messages. Has deafult value of False.")
    return parser


def get_args():
    parser = get_parser()
    args = parser.parse_args()

    return args
