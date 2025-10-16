import sys
from analytics import Research, Analytics
import config

if __name__ == "__main__":
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print("Data:", data)

        analytics = Analytics(data)
        heads, tails = analytics.counts()
        print("Counts:", heads, tails)

        h_frac, t_frac = analytics.fractions(heads, tails)
        print("Fractions:", h_frac, t_frac)

        predictions = analytics.predict_random(config.num_of_steps)
        print("Random predictions:", predictions)

        last_observation = analytics.predict_last()
        print("Last observation:", last_observation)

        # Save results
        analytics.save_file(data, config.report_file_name, 'txt')

        # Send Telegram notification
        research.send_telegram_message("The report has been successfully created")

    except IndexError:
        print("Usage: python3 make_report.py <path_to_csv>")
        
    except Exception as e:
        print(f"Error: {e}")
        research.send_telegram_message("The report hasn't been created due to an error.")
