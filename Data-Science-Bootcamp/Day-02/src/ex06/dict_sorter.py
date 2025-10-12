def get_country_data():
    """
    data
    """
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    
    country_dict = {}
    for country, number in list_of_tuples:
        country_dict[country] = number
    
    return country_dict


def sort_countries():
    country_dict = get_country_data()
    sorted_countries = sorted(country_dict.items(), key=lambda item: (-int(item[1]), item[0]))
    return [country for country, number in sorted_countries]


def display_sorted_countries():
    sorted_countries = sort_countries()
    for country in sorted_countries:
        print(country)


def main():
    display_sorted_countries()


if __name__ == '__main__':
    main()