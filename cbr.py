import argparse
import pandas as pd
import sys


# Dicts zum Mappen der Ausprägungen auf numerische Werte


def map_attribute(attrib: str) -> dict:
    # Spalte 'Zimmerzahl'
    match attrib:
        case "Zimmerzahl":
            return {'Zwei Zimmer': 2, '4 Zimmer': 4, 'Ein Zimmer': 1, '6 Zimmer': 6, '2-3 Zimmer': 2.5, '5 Zimmer': 5,
                    '3-4 Zimmer': 3.5, '4-5 Zimmer': 4.5, '5-6 Zimmer': 5.5, '3 Zimmer': 3}
        case "Stockwerk":
            return {'1.Stock': 1, '3.Stock': 3, 'EG': 0, '2.Stock': 2, '5.Stock': 5, '4.Stock': 4, '8.Stock': 8,
                    '9.Stock': 9,
                    '6.Stock': 6, '7.Stock': 7, '10.Stock': 10}
        case "Kindergarten":
            return {'nah': 1, 'erreichbar': 2, 'fern': 3}

        # Distanzen wobei 'nah' die geringste Distanz, 'erreichbar' eine mittlere und 'fern' die größte Distanz
        # bezeichnet.
        case "Schule":
            return {'nah': 1, 'erreichbar': 2, 'fern': 3}

        case "S-Bahn":
            return {'nah': 1, 'erreichbar': 2, 'mit Bus': 3, 'nein': 4}

        case "Miete":
            return {'251-300': 275, '551-600': 575, '751-800': 775, '401-450': 425, '201-250': 225, '651-700': 675,
                    '501-550': 525,
                    '601-650': 625, '801-850': 825, '701-750': 725, '451-500': 475, '901-950': 925, '851-900': 875}

        case "Nebenkosten":
            return {'50-100': 75, '201-250': 225, '151-200': 175, 'unter 50': 25, '251-300': 275, '101-150': 125,
                    'über 300': 325}

        case "Alter":
            return {'16-20 Jahre': 18, '4-7 Jahre': 5.5, '7-10 Jahre': 8.5, '11-15 Jahre': 13, '31-50 Jahre': 40.5,
                    'ueber 100': 100,
                    'Neubau': 0, '51-75 Jahre': 63, '1-3 Jahre': 2, '76-100 Jahre': 88, '21-30 Jahre': 25.5}

        case "Entfernung":
            return {'< 1 km': 0.5, '5-10 km': 7.5, '21-30 km': 25.5, '< 3 km': 1.5, '3-5 km': 4, '> 30 km': 35.5,
                    '11-20 km': 15.5}

        case "Kaution":
            return {'keine': 0, 'ueber 3000': 3500, '1000-1500': 1250}

        case "Moebliert":
            return {'nein': 0, 'teilmoebliert': 1, 'ja': 2}

        case "Quadratmeter":
            return {'31-40': 35.5, '91-100': 95.5, '81-90': 85.5, '20-30': 25.5, 'über 120': 125, '51-60': 55.5,
                    '101-110': 105.5,
                    '71-80': 75.5, '111-120': 115.5, '61-70': 65.5, '41-50': 45.5}

        case "Deckenhöhe":
            return {'250': 250, '260': 260, '280': 280, '300': 300}

    return {}


############################################ Similarity Functions ############################################
def similiarity_simple(x, y) -> float:
    diff = abs(x - y)
    # Berechnung der Ähnlichkeit als inverse Funktion der Differenz
    similarity = 1 / (1 + diff)

    return similarity


def similiarity_yes_no(x, y) -> bool:
    if x == y:
        return True
    return False


def similiarity_relative_to_interval(dict_values: dict, x, y) -> float:
    diff = abs(x - y)
    max_distance = max(dict_values.values()) - min(dict_values.values())
    relative_distance = diff / max_distance
    return 1 - relative_distance


def get_absolute_similiarity_to_case(case1: dict, case2: dict) -> float:
    # Berechnung der Ähnlichkeiten für jeden Fall in der Fallbasis
    similarity = 0
    for key, value in case1.items():
        if case2[key]:
            map_dict = map_attribute(key)
            if key == 'Zimmerzahl':
                # Informierte Ähnlichkeit: Berücksichtigung der Alternativenanzahl
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value],
                                                               map_dict[case2[key]]) * len(
                    map_dict.keys())
            elif key == 'Stockwerk':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value],
                                                               map_dict[case2[key]])
            elif key == 'Heizung':
                similiarity_yes_no(value, case2[key])
            elif key == 'Hausmeister':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Kindergarten':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value],
                                                               map_dict[case2[key]])
            elif key == 'Schule':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value], map_dict[case2[key]])
            elif key == 'S-Bahn':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value], map_dict[case2[key]])
            elif key == 'Garage':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Miete':
                similarity += similiarity_simple(map_dict[value], map_dict[case2[key]])
            elif key == 'Nebenkosten':
                similarity += similiarity_simple(map_dict[value], map_dict[case2[key]])
            elif key == 'Alter':
                similarity += similiarity_simple(map_dict[value], map_dict[case2[key]])
            elif key == 'Entfernung':
                similarity += similiarity_simple(map_dict[value], map_dict[case2[key]])
            elif key == 'Kaution':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value],
                                                               map_dict[case2[key]])
            elif key == 'Deckenhöhe':
                # print(value)
                similarity += similiarity_relative_to_interval(map_dict, (map_dict[str(value)]),
                                                               (map_dict[(str(case2[key]))]))
            elif key == 'Moebliert':
                similarity += similiarity_relative_to_interval(map_dict, map_dict[value],
                                                               map_dict[case2[key]])
            elif key == 'Quadratmeter':
                similarity += similiarity_simple(map_dict[value], map_dict[case2[key]])
            elif key == 'Kueche':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Waschraum':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Balkon':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Abstellraum':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Aufzug':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Lage':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Kabelanschluss':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Terrasse':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Kehrwoche':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Bad':
                similarity += similiarity_yes_no(value, case2[key])
            elif key == 'Klasse':
                # print('Info: Klasse angegeben und ignoriert.')
                pass
            else:
                print(f"Key '{key}' not found!")
    return similarity


def get_most_similar_case_idx(wohnung: dict, df: pd.DataFrame) -> int:
    max_similarity = get_absolute_similiarity_to_case(wohnung, wohnung)
    # Berechnung der Ähnlichkeiten für jeden Fall in der Fallbasis
    highest_similiarity = 0
    index_of_highest_similiarity = 0
    warning_for_same_similarity_but_different_classes = False
    # Checken, ob zwei Fälle aus Fallbasis die gleiche Ähnlichkeit zum "Fall" haben. Dann warnen! Weil unpräzise.
    # keine Ähnlichkeit für die Ausprägung berechnen, wenn wohnung nicht diese Ausprägung hat.
    for i in range(len(df)):
        abs_similarity = get_absolute_similiarity_to_case(wohnung, dict(df.iloc[i]))
        y = abs_similarity / max_similarity
        if y > highest_similiarity:
            highest_similiarity = y
            index_of_highest_similiarity = i
            warning_for_same_similarity_but_different_classes = False
        elif y == highest_similiarity:
            if dict(df.iloc[index_of_highest_similiarity])["Klasse"] == dict(df.iloc[i])["Klasse"]:
                warning_for_same_similarity_but_different_classes = True

    if warning_for_same_similarity_but_different_classes:
        return -1
    return index_of_highest_similiarity


def fallbasis_bauen(df: pd.DataFrame, fallbasis) -> pd.DataFrame:
    # über df iterieren
    for i in range(len(df)):
        # wenn fallbasis leer ist, füge ersten Fall hinzu
        if len(fallbasis) == 0:
            fallbasis = pd.concat([fallbasis, df.iloc[i:i + 1]], ignore_index=True)
            # print(f"Fall {i} hinzugefügt.")
        else:
            # wenn fallbasis nicht leer ist, berechne Ähnlichkeit zu jedem Fall in fallbasis
            index_of_most_similiar_case = get_most_similar_case_idx(dict(df.iloc[i]), fallbasis)
            # finde ähnlichsten Fall
            most_similiar_case = dict(fallbasis.iloc[index_of_most_similiar_case])

            # wenn ähnlichster Fall nicht die gleiche Klasse hat, füge Fall hinzu
            if most_similiar_case['Klasse'] != df.iloc[i]['Klasse']:
                fallbasis = pd.concat([fallbasis, df.iloc[i:i + 1]], ignore_index=True)
                # print(f"Fall {i} hinzugefügt.")
            else:
                print(f"Fall {i} nicht hinzugefügt.")
                pass
    return fallbasis


def deduce_class(wohnung: dict, df: pd.DataFrame) -> str:
    index_of_most_similiar_case = get_most_similar_case_idx(wohnung, df)
    if index_of_most_similiar_case == -1:
        return "!Multiple classes have same similiarity to this case. Please try to be more precise!"
    most_similiar_case = dict(df.iloc[index_of_most_similiar_case])
    return most_similiar_case['Klasse']


############################################# Main Function ########################################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, help='input file path', required=True)
    # parser.add_argument('output_file', type=str)
    args = parser.parse_args()

    df = pd.read_csv(args.input_file, sep=';')
    df = df.sample(frac=1).reset_index(drop=True)
    fallbasis = pd.DataFrame(columns=df.columns)
    fallbasis = fallbasis_bauen(df, fallbasis)
    print(f"\n\n Hello, the casebase (size: {len(fallbasis)} cases) was successfully established. "
          f"You can now enter a case to check. "
          f"If you enter nothing, the attribute will be skipped. \n\n")

    while True:
        attributes = {}
        for i in range(df.columns.size - 1):
            attribute = df.columns[i]
            possible_vals = sorted(df[attribute].unique())
            possible_vals_map_str = ", ".join([f"{i}: '{possible_vals[i]}'" for i in range(len(possible_vals))])
            user_ipt = input(f"Enter number for attribute value {df.columns[i]}:\n "
                             f"{possible_vals_map_str}: ")

            if user_ipt == '':
                continue
            elif int(user_ipt) in range(len(possible_vals)):
                attributes[df.columns[i]] = possible_vals[int(user_ipt)]
            else:
                print(f"Error: Number '{user_ipt}' is not valid for attribute {df.columns[i]}.", file=sys.stderr)

        if len(attributes.keys()) == 0:
            print("No attributes entered. Aborting...", file=sys.stderr)
            exit(1)

        print(f"The deduced Class is {deduce_class(attributes, fallbasis)}!")
        yn = input("Do you want to continue? (y/n): ")
        if yn == 'y':
            continue
        else:
            break


if __name__ == '__main__':
    main()
