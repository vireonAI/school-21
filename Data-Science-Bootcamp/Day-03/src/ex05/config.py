num_of_steps = 3
report_template = (
    "We made {total} observations by tossing a coin: "
    "{tails} were tails and {heads} were heads. "
    "The probabilities are {tail_perc:.2f}% and {head_perc:.2f}%, respectively. "
    "Our forecast is that the next {num_of_steps} observations will be: "
    "{predicted_tails} tail(s) and {predicted_heads} head(s)."
)