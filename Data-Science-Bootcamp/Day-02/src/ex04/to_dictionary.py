def get_list_of_tuples():
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
    return list_of_tuples

def create_dictionary_from_tuples():
    list_of_tuples = get_list_of_tuples()
    result_dict = {}

    for country, number in list_of_tuples:
        if number in result_dict:
            result_dict[number].append(country)
        else:
            result_dict[number] = [country]

    return result_dict

def display_dictionary(dictionary):
    for key in dictionary:
        for country in dictionary[key]:
            print(f"'{key}':'{country}'")

def main():
    country_dict = create_dictionary_from_tuples()
    display_dictionary(country_dict)

if __name__ == "__main__":
    main()