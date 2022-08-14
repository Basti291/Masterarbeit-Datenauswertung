import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import statistics

# Define this before start
#main_source_folder = 'C:\\Users\\spraf\\IdeaProjects\\KITE\\KITE-Janustutorial-Test\\kite-allure-reports\\'
#main_source_folder = 'C:\\Users\\spraf\\IdeaProjects\\KITE\\KITE-AntMediaTest-Test\\kite-allure-reports\\'
#main_source_folder = 'C:\\Users\\spraf\\Desktop\\Studium\\Master\\Masterarbeit\\Programieren\\Janus\\Test\\Testergerbnisse\\Ant MEdia\\1-cpu-1gb\\kite-allure-reports\\'
main_source_folder = 'C:\\Users\\spraf\\Desktop\\Studium\\Master\\Masterarbeit\\Programieren\\Janus\\Test\\Testergerbnisse\\Janus\\4-cpu-8gb\\Test1.2\\kite-allure-reports\\'
main_json_name = main_source_folder + 'd419cf23-2efe-49c0-8541-aee0eb9ef37f-result.json'
number_of_clients = 150  # Sollte eine Zahl teilbar durch 10 sein, damit das Balkendiagramm richtig angezeigt wird
chart_scaling_x_axis = 10000  # Default auf 5000ms stellen: sagt, wie die x_achse gegliedert ist, also z.B ein Wert alle 5000 ms. So werden dann auch alle y-Werte innerhalb der 5000ms aggregiert
# Define until here
main_json = {}
rtc_stats = []
start_timestamp = 0
stop_timestamp = 0


def start():
    parse_main_json()
    parse_rtc_stats()

    build_video_check_statistics()
    build_latency_statstics()
    build_bitrate_video_statistics()
    build_bitrate_audio_statistics()
    build_jitter_audio_statistics()
    build_jitter_video_statistics()
    #build_packets_lost_audio_statistics()
    #build_packets_lost_video_statistics()


def build_video_check_statistics():
    global main_json
    parse_main_json()

    steps = main_json["steps"]
    counter_visible = 0
    counter_not_visible = 0

    bar_first, bar_second, bar_third, bar_fourth, bar_fifth, bar_sixth, bar_seventh, bar_eighth, bar_nineth, bar_tenth = [], [], [], [], [], [], [], [], [], []
    switcher = {
        0: bar_first,
        1: bar_second,
        2: bar_third,
        3: bar_fourth,
        4: bar_fifth,
        5: bar_sixth,
        6: bar_seventh,
        7: bar_eighth,
        8: bar_nineth,
        9: bar_tenth
    }
    for step in steps:
        if step["description"] == "Check if video is visible":
            if step["status"] == "PASSED":
                with open(main_source_folder + step["attachments"][0]["source"], 'r') as file:
                    current_video_check_json = json.load(file)
                if int(current_video_check_json["videoStartupTimeInMs"]) > 0:
                    counter_visible += 1
                    switcher[current_video_check_json["clientNumber"] % 10].append(
                        current_video_check_json["videoStartupTimeInMs"])
                else:
                    counter_not_visible += 1
                    switcher[int(step["name"][-28]) % 10].append(-250)
            else:
                switcher[int(step["name"][-28]) % 10].append(-250)
                counter_not_visible += 1
    counted = counter_visible + counter_not_visible
    if counted != number_of_clients:
        print("ERROR: die gezählten Videochecks waren stimmen nicht mit der angegebenen Anzahl von CLients überein. "
              "Angegebene Anzahl Clients: ", number_of_clients, " visibleVideos: ", counter_visible,
              "notVisibleVideos: ", counter_not_visible)

    # Pie Chart
    labels = 'Sichtbar', 'Nicht sichtbar'
    sizes = [counter_visible / counted, counter_not_visible / counted]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('pie_chart.png')
    plt.show()

    # Bar Chart
    bar_median = []
    bar_max = []
    for index in range(len(bar_first)):
        newList = []
        newList.append(bar_first[index])
        if len(bar_second) > index:
            newList.append(bar_second[index])
        if len(bar_third) > index:
            newList.append(bar_third[index])
        if len(bar_fourth) > index:
            newList.append(bar_fourth[index])
        if len(bar_fifth) > index:
            newList.append(bar_fifth[index])
        if len(bar_sixth) > index:
            newList.append(bar_sixth[index])
        if len(bar_seventh) > index:
            newList.append(bar_seventh[index])
        if len(bar_eighth) > index:
            newList.append(bar_eighth[index])
        if len(bar_nineth) > index:
            newList.append(bar_nineth[index])
        if len(bar_tenth) > index:
            newList.append(bar_tenth[index])
        #bar_median.append(statistics.median(newList))
        #bar_max.append(max(newList))

    bar_labels = np.arange(1, number_of_clients / 10 + 1, dtype=int)
    width = 0.8
    fig2, ax2 = plt.subplots()

    rects1 = ax2.bar(bar_labels - 1 * width / 10, bar_first, width / 10, label='1')
    rects2 = ax2.bar(bar_labels - 2 * width / 10, bar_second, width / 10, label='2')
    rects3 = ax2.bar(bar_labels - 3 * width / 10, bar_third, width / 10, label='3')
    rects4 = ax2.bar(bar_labels - 4 * width / 10, bar_fourth, width / 10, label='4')
    rects5 = ax2.bar(bar_labels - 5 * width / 10, bar_fifth, width / 10, label='5')
    rects6 = ax2.bar(bar_labels + 4 * width / 10, bar_sixth, width / 10, label='6')
    rects7 = ax2.bar(bar_labels + 3 * width / 10, bar_seventh, width / 10, label='7')
    rects8 = ax2.bar(bar_labels + 2 * width / 10, bar_eighth, width / 10, label='8')
    rects9 = ax2.bar(bar_labels + 1 * width / 10, bar_nineth, width / 10, label='9')
    rects10 = ax2.bar(bar_labels, bar_tenth, width / 10, label='10')
    #rects_median = ax2.bar(bar_labels + 5 * width / 10, bar_median, width / 10, label='Median')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Zeit in Millisekunden')
    ax2.set_xlabel('Nummer des Ramp-Ups')
    ax2.set_title('Dauer bis das Video zu sehen ist, gruppiert nach Nummer des Ramp-Ups')
    ax2.set_xticks(bar_labels, bar_labels)
    #ax2.legend()
    #for index in range(len(bar_median)):
        #plt.text(bar_labels[index], bar_max[index], "Median: " + str(bar_median[index]), ha='center', fontsize=12)

    fig2.tight_layout()
    plt.savefig('startupt_times.png')
    plt.show()


def build_latency_statstics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='latencyInMs')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Latenz in Millisekunden')
    plt.title('Verlauf der Durchschnittslatenz aller Clients im zeitlichen Verlauf')
    plt.savefig('latency.png')
    plt.show()


def build_bitrate_video_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/video',
                                                                            second_key='video-bitrate-in-kbit-per'
                                                                                       '-second')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Bitrate in kbit/s')
    plt.title('Verlauf der Durchschnittsbitrate des Videos aller Clients im zeitlichen Verlauf')
    plt.savefig('video_bitrate.png')
    plt.show()


def build_bitrate_audio_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/audio',
                                                                            second_key='audio-bitrate-in-kbit-per-second')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Bitrate in kbit/s')
    plt.title('Verlauf der Durchschnittsbitrate des Audios aller Clients im zeitlichen Verlauf')
    plt.savefig('audio_bitrate.png')
    plt.show()


def build_jitter_audio_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/audio',
                                                                            second_key='jitter')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Jitter in')
    plt.title('Verlauf des Durchschnitts-Jitter des Audios aller Clients im zeitlichen Verlauf')
    plt.savefig('audio_jitter.png')
    plt.show()


def build_jitter_video_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/video',
                                                                            second_key='jitter')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Jitter in')
    plt.title('Verlauf des Durchschnitts-Jitter des Videos aller Clients im zeitlichen Verlauf')
    plt.savefig('video_jitter.png')
    plt.show()


def build_packets_lost_audio_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/audio',
                                                                            second_key='packetsLost')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Absolute Anzahl Verlorener Pakete')
    plt.title('Verlorene Pakete des Audios aller Clients im Durchschnitt im zeitlichen Verlauf (kummuliert)')
    plt.savefig('audio_packets_lost.png')
    plt.show()


def build_packets_lost_video_statistics():
    x_axis, y_axis, milliseconds_in_readable_time = build_general_statistic(first_key='inbound-rtp/video',
                                                                            second_key='packetsLost')
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Absolute Anzahl Verlorener Pakete')
    plt.title('Verlorene Pakete des Videos aller Clients im Durchschnitt im zeitlichen Verlauf (kummuliert)')
    plt.savefig('video_packets_lost.png')
    plt.show()


def build_general_statistic(**key_names):
    global main_json
    global rtc_stats
    parse_main_json()
    parse_rtc_stats()
    x_axis, y_axis, y_axis_count = prepare_x_and_y_axis()
    for stat in rtc_stats:
        if "inbound-rtp/video" not in stat:
            continue
        timestamp_received = int(stat["inbound-rtp/video"]["timestamp"])
        position_in_x_axis = int((timestamp_received - start_timestamp) / chart_scaling_x_axis)
        if len(key_names) == 1:
            y_axis[position_in_x_axis] += int(stat[key_names["first_key"]])
        else:
            try:
                val = int(stat[key_names["first_key"]][key_names["second_key"]])
            except ValueError:
                val = float(stat[key_names["first_key"]][key_names["second_key"]])

            y_axis[position_in_x_axis] += val

        y_axis_count[position_in_x_axis] += 1

    milliseconds_in_readable_time = []
    for index in range(len(y_axis)):
        if index % 30 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")
        if y_axis_count[index] > 0:
            y_axis[index] = y_axis[index] / y_axis_count[index]

    return x_axis, y_axis, milliseconds_in_readable_time


def parse_main_json():
    global main_json
    global main_json_name

    if main_json != {}:
        return
    with open(main_json_name, 'r') as file:
        main_json = json.load(file)
    # pretty_print_json(main_json)
    global start_timestamp
    global stop_timestamp
    start_timestamp = int(main_json["start"])
    stop_timestamp = int(main_json["stop"])


def parse_rtc_stats():
    global main_json
    global rtc_stats
    global start_timestamp
    global stop_timestamp
    if rtc_stats:
        return
    if main_json != {}:
        parse_main_json()

    steps = main_json["steps"]
    counter_passed = 0
    rtc_stats_file_names = []
    for step in steps:
        if step["description"] == "Collect Stats ":
            start_timestamp = min(start_timestamp, step["start"])
            stop_timestamp = max(stop_timestamp, step["stop"])
            if step["status"] == "PASSED":
                counter_passed += 1
                rtc_stats_file_names.append(step["attachments"])
            else:
                print("ERROR: ", step["name"], "ist fehlgeschlagen!")

    for client in rtc_stats_file_names:
        for stat in client:
            with open(main_source_folder + stat["source"], 'r') as file:
                current_stats_file = json.load(file)
            rtc_stats.append(current_stats_file)
    pretty_print_json(rtc_stats)


def prepare_x_and_y_axis():
    test_duration = stop_timestamp - start_timestamp
    x_axis = np.arange(0, test_duration, chart_scaling_x_axis).tolist()
    y_axis = []
    y_axis.extend([0] * len(x_axis))
    y_axis_count = []
    y_axis_count.extend([0] * len(x_axis))
    return x_axis, y_axis, y_axis_count


def pretty_print_json(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True))


def convert_millis(millis):
    seconds = int((millis / 1000) % 60)
    minutes = int((millis / (1000 * 60)) % 60)
    return to_string_time(minutes) + ":" + to_string_time(seconds)


def to_string_time(time):
    if time < 10:
        return "0" + str(time)
    else:
        return str(time)


def get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time):
    new_x_axis = []
    new_labels = []
    for i, num in enumerate(x_axis):
        if num % 60000 == 0:
            new_x_axis.append(num)
            new_labels.append(milliseconds_in_readable_time[i])

    return new_x_axis, new_labels


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

