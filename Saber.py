
import csv

# This takes some time to process
def get_data():
    file = open('data.csv','r')
    read = csv.reader(file)
    data = list(read)
    file.close()
    return data

# COLUMN NUMBERS
#7 - Event Code
#8 - wOBA points
#23 - Pitch Sequence
#38 - Runner on First final destination
#39 - Runner on Second final destination
#40 - Runner on Third final destination

# PITCH SEQUENCE SYMBOLS
# > - Runner Stealing on the Pitch
# X - Ball put into play
# S - Swinging Strike
# F - Foul Ball
# Q - Swing on Pitchout
# R - Foul ball on Pitchout
# T - Foul tip out

# EVENT CODES
# 2 - Generic out
# 4 - Stolen base
# 6 - Caught Stealing
# 17 - Interference
# 18 - Error
# 19 - Fielder's Choice
# 20 - Single
# 21 - Double
# 22 - Triple
# 23 - Home Run

# Gets all hit and run plays and stores them in a new list
def get_hnr():
    hnr_data = []
    for row in data:
        if ('>X' in row[23] or '>S' in row[23] or
            '>F' in row[23] or '>Q' in row[23] or
            '>R' in row[23] or '>T' in row[23]):
            if(row[8]):
                hnr_data.append(row)
            elif (row[7] == '4' or row[7] == '6'):
                hnr_data.append(row)
    return hnr_data

# Hit and Run Success rate. A success is considered any time
# a HnR attempt ends with a runner advancing
def hnr_success(hnr_data):
    hit_count = 0
    tot_count = 0
    for row in hnr_data:
        if('>X' in row[23]):
            event = row[7]
            if (event == '20' or event == '21' or
                event == '22' or event == '23' or
                event == '18' or event == '17'):
                hit_count += 1
                tot_count += 1
            elif (event == '19'):
                tot_count += 1
            elif (event == '2'):
                if (row[38] == '2' or row[38] == '3' or
                    row[38] == '4' or row[39] == '3' or
                    row[39] == '4' or row[40] == '4'):
                    hit_count += 1
                    tot_count += 1
                else:
                    tot_count += 1
        elif event == '4':
            hit_count += 1
        elif event == '6':
            tot_count += 1

    success_rate = hit_count/tot_count
    return success_rate

# Batting average on At-Bats which include
# at least one HnR attempt.
# League avg 2005-215 = .259
def hnr_bat_avg(hnr_data):
    hit_count = 0
    ab_count = 0
    i = 0
    for row in hnr_data:
        event = row[7]
        if (event == '20' or event == '21' or
            event == '22' or event == '23'):
            hit_count += 1
            ab_count += 1
        elif (event == '4' or event == '6' or
              event == '14' or event == '15'):
                continue
        else:
            ab_count += 1
    avg = hit_count/ab_count
    return avg

# Calculates wOBA for HnR at bats
def hnr_woba(hnr_data):
    woba_count = 0
    ab_count = 0
    for row in hnr_data:
        try:
            woba_count += float(row[8])
        except ValueError:
            continue
        ab_count += 1
    woba = woba_count/ab_count
    return woba

# Calculates wRC+ for HnR at bats
def hnr_wrc(woba):
    hnr_woba = woba
    league_woba = 0.321
    woba_scale = 1.23481818
    league_rpa = 0.11654545
    park_factor = 1
    wrc_pa = (115919/970159)

    wrc = (((((hnr_woba-league_woba)/woba_scale) + league_rpa) +
           (league_rpa - park_factor * league_rpa))/(wrc_pa))*100

    return wrc

# Main Script
data = get_data()
hnr_data = get_hnr()

success_rate = hnr_success(hnr_data)
print("\nHit and Run success rate: "+str(success_rate)+'\n')

avg = hnr_bat_avg(hnr_data)
print("BA for AB with HnR attempts: "+str(avg))
print("League Average BA 2005-2015: .259\n")

woba = hnr_woba(hnr_data)
print("wOBA for AB with HnR attempts: "+str(woba))
print("League Average wOBA 2005-2015: .321\n")

wrc = hnr_wrc(woba)
print("wRC+ for AB with HnR attempts: "+str(wrc))
print("League Average wRC+ is always 100")
