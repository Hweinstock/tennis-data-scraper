from data_collector import DataCollector
from args import get_args

def main():
    args = get_args()
    data_collector_obj = DataCollector(args.debug)
    if args.debug:
        print("Got arguments "+str(args.years)+", "+str(args.players)+", "+args.mode+", "+str(args.singles))
    data_collector_obj.scrape_last_n_years_of_k_players(args.years, args.players, args.mode, "singles" if args.singles else "doubles")

if __name__ == '__main__':

    """
    Testing
    python3 main.py #years #players mode sing/dubs debug
    """

    main()



    #args["obj"].scrape_last_n_years_of_k_players(args["n"], args["k"], args["mode"], args["singOrDubs"], args["debug"])
    #dc = DataCollector(True)
    #dc.scrape_last_n_years_of_k_players(2, 10, "basic-info", "singles")
    #dc.scrape_last_n_years_of_k_players(2, 10, "marital_status", "singles")
