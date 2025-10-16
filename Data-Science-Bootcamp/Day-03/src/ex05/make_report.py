import sys
from analytics import Research, Analytics
import config

if __name__ == "__main__":
    try:
        research = Research(sys.argv[1])
        data = research.file_reader() 

        analytics = Analytics(data)
        heads, tails = analytics.counts()
        head_frac, tail_frac = analytics.fractions(heads, tails)

        predictions = analytics.predict_random(config.num_of_steps)
        predicted_heads = sum(1 for p in predictions if p == [1, 0])
        predicted_tails = sum(1 for p in predictions if p == [0, 1])

        report_text = config.report_template.format(
            total=len(data),
            tails=tails,
            heads=heads,
            tail_perc=tail_frac * 100,
            head_perc=head_frac * 100,
            num_of_steps=config.num_of_steps,
            predicted_tails=predicted_tails,
            predicted_heads=predicted_heads
        )

        analytics.save_file(report_text, "report", "txt")

        print(report_text)

    except IndexError:
        print("Usage: python3 make_report.py <path_to_csv>")
    except Exception as e:
        print(f"Error: {e}")
