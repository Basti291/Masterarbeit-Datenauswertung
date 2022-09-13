import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import statistics

# Define this before start
#main_source_folder = 'C:\\Users\\spraf\\IdeaProjects\\KITE\\KITE-Janustutorial-Test\\kite-allure-reports\\'
#main_source_folder = 'C:\\Users\\spraf\\IdeaProjects\\KITE\\KITE-AntMediaTest-Test\\kite-allure-reports\\'
main_source_folder = 'C:\\Users\\spraf\\Desktop\\Studium\\Master\\Masterarbeit\\Programieren\\Janus\\Test\\Testergerbnisse\\Ant MEdia\\1-cpu-1gb\\kite-allure-reports\\'
#main_source_folder = 'C:\\Users\\spraf\\Desktop\\Studium\\Master\\Masterarbeit\\Programieren\\Janus\\Test\\Testergerbnisse\\Janus\\4-cpu-8gb\\Test2\\kite-allure-reports\\'
main_json_name = main_source_folder + 'd70f621b-a6bc-422b-9f24-30cc413b087f-result.json'
number_of_clients = 17  # Sollte eine Zahl teilbar durch 10 sein, damit das Balkendiagramm richtig angezeigt wird
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
                print(current_video_check_json["videoStartupTimeInMs"])
                if int(current_video_check_json["videoStartupTimeInMs"]) > 0:
                    counter_visible += 1
                    switcher[current_video_check_json["clientNumber"] % 10].append(
                        current_video_check_json["videoStartupTimeInMs"])
                else:
                    counter_not_visible += 1
                    switcher[int(step["name"][-28]) % 10].append(-20)
            else:
                switcher[int(step["name"][-28]) % 10].append(-20)
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
    #ax2.set_title('Dauer bis das Video zu sehen ist, gruppiert nach Nummer des Ramp-Ups')
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
    #plt.title('Verlauf der Durchschnittslatenz aller Clients im zeitlichen Verlauf')
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
    #plt.title('Verlauf der Durchschnittsbitrate des Videos aller Clients im zeitlichen Verlauf')
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
    #plt.title('Verlauf der Durchschnittsbitrate des Audios aller Clients im zeitlichen Verlauf')
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
    plt.ylabel('Jitter')
    #plt.title('Verlauf des Durchschnitts-Jitter des Audios aller Clients im zeitlichen Verlauf')
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
    plt.ylabel('Jitter')
    #plt.title('Verlauf des Durchschnitts-Jitter des Videos aller Clients im zeitlichen Verlauf')
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
    #plt.title('Verlorene Pakete des Audios aller Clients im Durchschnitt im zeitlichen Verlauf (kummuliert)')
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
    #plt.title('Verlorene Pakete des Videos aller Clients im Durchschnitt im zeitlichen Verlauf (kummuliert)')
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


def build_default_pie_chart():
    # Pie Chart
    labels = 'Sichtbar', 'Nicht sichtbar'
    sizes = [66/80, 13/80]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('pie_chart.png')
    plt.show()





# ------------------------ AB HIER FOLGEN DIE DIAGRAMME DES SERVERS MIT DEN DATEN VON DIGITAL OCEAN --------------------------------





def build_server_cpu_chart_janus():
    x_axis = range(0, 1800000+36*30000)
    x_axis = x_axis[::30000]
    y_axis2 = [3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 13, 13, 16, 16, 18.5, 18.5, 21, 21, 24, 24, 26, 26, 29.5, # Janus 1-cpu-1gb-Test1
              29.5, 32.5, 32.5, 36, 36, 39.5, 39.5, 40.5, 40.5, 41, 41, 40.8, 40.8, 40.6, 40.6, 42, 42, 44, 44, 49, 49,
              55, 55, 50, 50, 45, 45, 43.5, 43.5, 42, 42, 41.5, 41.5, 41, 41, 41.1, 41.1, 41.2, 41.2, 43, 43, 44, 44,
              45, 45, 46, 46, 43, 43, 40, 40, 38, 38, 36, 36, 26, 26, 14, 14, 8, 8, 2, 2, 1, 1, 1, 1, 1]
    y_axis3 = [2.5, 3.5, 3.5, 4.8, 4.8, 6.5, 6.5, 7, 7, 8, 8, 9.5, 9.5, 10.5, 10.5, 12.5, 12.5, 14.8, 14.8, 17, 17, 18.5, 18.5, # Janus 2-cpu-4gb-Test1
                22, 22, 24.5, 24.5, 26.5, 26.5, 28.5, 28.5, 28, 28, 27.5, 27.5, 28.5, 28.5, 29.5, 29.5, 28.3, 28.3, 27,
                27, 28.5, 28.5, 29.5, 29.5, 31, 31, 32, 32, 27.5, 27.5, 23.5, 23.5, 27, 27, 30, 30, 29.7, 29.7, 29.2, 29.2,
                29.8, 29.8, 30, 30, 27, 27, 23.5, 23.5, 25.2, 25.2, 27, 27, 25.2, 25.2, 24, 24, 16, 16, 7.5, 7.5, 5, 5,
                2.2, 2.2, 1.9, 1.9, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7]
    y_axis = [1, 1.8, 1.8, 2.3, 2.3, 3, 3, 4, 4, 4.1, 4.1, 4.2, 4.2, 5.2, 5.2, 6.5, 6.5, 6.7, 6.7, 6.8, 6.8, 7.7, 7.7, # janus 4-cpu-4gb
              8.5, 8.5, 8.3, 8.3, 8, 8, 9.8, 9.8, 11.8, 11.8, 11.7, 11.7, 11.6, 11.6, 11.2, 11.2, 10.8, 10.8, 10.7,
              10.7, 10.6, 10.6, 10.4, 10.4, 10.2, 10.2, 10.6, 10.6, 11, 11, 11.4, 11.4, 11.6, 11.6, 11.5, 11.5, 11.5,
              11.5, 13, 13, 14.8, 14.8, 14, 14, 13.3, 13.3, 15, 15, 17, 17, 16.5, 16.5, 16, 16, 16.8, 16.8, 17.7, 17.7,
              15.3, 15.3, 12.5, 12.5, 7.5, 7.5, 2.5, 2.5, 2, 2, 1.5, 1.5, 1, 1, 1]

    milliseconds_in_readable_time = []

    for index in range(len(x_axis)):
        if index % 10 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    fig.set_size_inches(12, 8)
    ax.plot(x_axis, y_axis, label='4 CPU\'s (150 Empfänger)')  # Plot some data on the axes.
    ax.plot(x_axis, y_axis3, label='2 CPU\'s (150 Empfänger)')
    ax.plot(x_axis, y_axis2, label='1 CPU\'s (150 Empfänger)')
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('CPU-Auslastung in %')
    plt.legend()
    plt.savefig('CPU-Auslastung-Janus.png', bbox_inches='tight')
    plt.show()


def build_server_cpu_chart_ant():
    x_axis = range(0, 32*60000)
    x_axis = x_axis[::30000]
    y_axis2 = [17, 33, 33, 50, 50, 53, 53, 56, 56, 56.5, 56.5, 57, 57, 57.3, 57.3, 57.6, 57.6, 51, 51, # 1-cpu-1gb Test 1
               45, 45, 23, 23, 7, 7, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    y_axis3 = [10, 23, 23, 23, 37, 37, 54, 54, 54, 70, 70, 68, 68, 67, 67, 67.5, 67.5, 68, 68, 64, 64, # 2-cpu-4-gb Test1
               57, 57, 63, 63, 63, 65, 65, 66, 67, 67, 62, 62, 55, 55, 38, 38, 15, 15, 12, 12, 12, 10, 10,
               10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    y_axis = [14, 26, 26, 29, 29, 44, 44, 51, 51, 60, 60, 69, 69, 72, 72, 78, 78, 78.5, 78.5, 79, 79, 79.5, 79.5, 80,
              80, 80.5, 80.5, 81, 81, 80.8, 80.8, 80.4, 80.4, 81, 81, 81.5, 81.5, 82, 82, 82.5, 82.5, 81, 81, 80, 80,
              78.5, 78.5, 77.5, 77.5, 52, 52, 34, 34, 20, 20, 12, 12, 11, 11, 11, 0, 0, 0, 0]

    milliseconds_in_readable_time = []

    for index in range(len(x_axis)):
        if index % 10 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis, label='4 CPU\'s (80 Empfänger)')  # Plot some data on the axes.
    ax.plot(x_axis, y_axis3, label='2 CPU\'s (40 Empfänger)')
    ax.plot(x_axis, y_axis2, label='1 CPU\'s (17 Empfänger)')
    fig.set_size_inches(12, 8)
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('CPU-Auslastung in %')
    plt.legend()
    plt.savefig('CPU-Auslastung-Ant-Media.png', bbox_inches='tight')
    plt.show()


def build_server_ram_chart_ant():
        x_axis = range(0, 32 * 60000)
        x_axis = x_axis[::30000]
        # 1-cpu_1gb Test 1
        y_axis2 = [27, 27, 57, 57, 60, 60, 65, 65, 90, 90, 93, 93, 95, 95, 95, 95,95, 93, 93, 90, 90, 90, 90, 90, 90,
                   90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
                   90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
        y_axis3 = [19, 19, 20, 20, 23, 23, 25.5, 25.5, 34, 34, 40, 40, 42, 42, 42.5, 42.5, 42.8, 42.8, 42.8, 42.8,
                   43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 42.8, 42.8, 42.5, 42.5, 42.5,
                   42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5, 42.5,
                   42.5, 42.5, 42.5, 42.5, 42.5, 42.5]
        y_axis = [12, 12, 13, 13, 14, 14, 14, 14, 15, 15, 19, 19, 23.5, 23.5, 28.5, 28.5, 33, 33, 34.5, 34.5, 36, 36,
                  38, 38, 40, 40, 40.5, 40.5, 41, 41, 42, 42, 42.5, 42.5, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42,
                  42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42]

        milliseconds_in_readable_time = []

        for index in range(len(x_axis)):
            if index % 10 == 0:
                milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
            else:
                milliseconds_in_readable_time.append("")

        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.plot(x_axis, y_axis, label='8 GB RAM (80 Empfänger)')  # Plot some data on the axes.
        ax.plot(x_axis, y_axis3, label='4 GB RAM (40 Empfänger)')
        ax.plot(x_axis, y_axis2, label='1 GB RAM (17 Empfänger)')
        fig.set_size_inches(12, 8)
        new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
        plt.xticks(new_x_axis, new_labels)
        plt.xlabel('Vergangene Zeit in Minuten')
        plt.ylabel('RAM-Auslastung in %')
        plt.legend()
        plt.savefig('RAM-Auslastung-Ant-Media.png', bbox_inches='tight')
        plt.show()


def build_server_ram_chart_janus():
    x_axis = range(0, 1800000+36*30000)
    x_axis = x_axis[::30000]
    # janus 1cpu-1gb test 1
    y_axis2 = [24.5, 24.5, 25, 25, 26.5, 26.5, 27.5, 27.5, 28.5, 28.5, 29.5, 29.5, 31, 31, 32, 32, 33, 33, 33.5, 33.5,
               33.8, 33.8, 34, 33, 33.8, 33.8, 34, 34, 33.8, 33.8, 33.8, 33.8, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,
               34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,
               34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,
               34, 34, 34, 32.5, 32.5]
    y_axis3 = [8.5, 8.5, 8.8, 8.8, 9.1, 9.1, 9.4, 9.4, 9.7, 9.7, 10, 10, 10.3, 10.3, 10.6, 10.6, 10.9, 10.9, 11.2, 11.2,
               11.2, 11.2, 11.2, 11.4, 11.4, 11.6, 11.6, 11.4, 11.4, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2,11.2,
               11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2,
               11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2,
               11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2,
               11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 11.2, 10.5, 10.5]
    y_axis = [5.9, 5.9, 5.9, 5.9, 5.9, 6, 6, 6, 6, 6, 6.1, 6.1, 6.1, 6.1, 6.1, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2,
              6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2,
              6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2,
              6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2,
              6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6.2, 6, 6]

    milliseconds_in_readable_time = []

    for index in range(len(x_axis)):
        if index % 10 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    fig.set_size_inches(12, 8)
    ax.plot(x_axis, y_axis, label='8 GB RAM (150 Empfänger)')  # Plot some data on the axes.
    ax.plot(x_axis, y_axis3, label='4 GB RAM (150 Empfänger)')
    ax.plot(x_axis, y_axis2, label='1 GB RAM (150 Empfänger)')
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('RAM-Auslastung in %')
    plt.legend()
    plt.savefig('RAM-Auslastung-Janus.png', bbox_inches='tight')
    plt.show()

def build_server_bandbreite_chart_janus():
    x_axis = range(0, 1800000+36*30000)
    x_axis = x_axis[::30000]
    # janus 1cpu-1gb test 1
    y_axis2 = [0, 0, 2, 2, 2, 5, 5.5, 6, 9, 9.5, 10, 15, 16, 17, 20, 20, 25, 26, 27, 30, 31, 37, 38, 38, 43, 43, 43, 50,
               50, 50, 53, 54, 54, 54, 58, 58, 58, 58, 58, 58, 62, 62, 62, 64, 64, 64, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 64, 64, 64,
               61.5, 61.5, 61.5, 60, 60, 60, 60, 60, 60, 61, 61, 61, 62, 62, 62, 62, 62, 62, 62, 60.5, 60.5, 60.5, 51, 51, 51, 35, 35, 35, 19, 19,
               19, 5, 5, 5, 0]
    y_axis3 = [0, 0, 2, 2, 2, 4, 4.5, 5, 9, 9.5, 10, 17.5, 18, 18.5, 23, 24, 25, 32, 33, 34, 40, 41, 42, 45, 45, 48,
               48, 48, 50, 52, 52, 52, 53, 54, 54, 54, 57, 57, 60, 60, 60, 61, 61, 62, 62, 62, 63, 63, 63, 64, 64,
               66, 66, 66, 64, 64, 64, 64, 64, 63, 63, 63, 63, 63, 62, 62, 61, 61, 61, 59, 59, 59, 59,
               59, 60, 60, 59, 59, 59, 48, 48, 48, 45, 45, 35, 35, 35, 27, 27, 20, 20, 20, 7, 7, 0, 0]
    y_axis = [0, 0, 3, 3, 3, 3.5, 8, 8, 8, 9, 16, 16, 16, 20, 20, 23, 23, 23, 28, 32, 32, 32, 36, 39, 39, 39, 41, 46,
              46, 46, 50, 50, 56, 56, 56, 59, 61, 61, 61, 65, 65, 64, 64, 64, 65, 65, 65, 65, 64, 64, 62, 62, 62, 60,
              60, 62, 62, 62, 63, 65, 65, 65, 65, 65, 65, 67, 67, 66, 66, 66, 64, 64, 64, 64, 60, 60, 58, 54, 54, 54, 41, 41, 41,
              35, 35, 25, 25, 25, 17, 14, 14, 14, 2, 2, 0, 0]

    milliseconds_in_readable_time = []

    for index in range(len(x_axis)):
        if index % 10 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    fig.set_size_inches(12, 8)
    ax.plot(x_axis, y_axis, label='4 CPU\'s (150 Empfänger)')  # Plot some data on the axes.
    ax.plot(x_axis, y_axis3, label='2 CPU\'s (150 Empfänger)')
    ax.plot(x_axis, y_axis2, label='1 CPU\'s (150 Empfänger)')
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Bandbreite in Mb/s')
    plt.legend()
    plt.savefig('Bandbreite-Janus.png', bbox_inches='tight')
    plt.show()


def build_server_bandbreite_chart_ant():
    x_axis = range(0, 32*60000)
    x_axis = x_axis[::30000]
    # 1-cpu-1gb
    y_axis2 = [0, 0, 2, 2, 6, 6, 11, 11, 15, 15, 18, 18, 18, 18, 14, 14, 9.5, 9.5, 5, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    y_axis3 = [0, 0, 2, 2.2, 2.4, 8.3, 8.6, 8.9, 15, 16, 17, 22, 23, 24, 28, 30, 32, 32, 36, 36, 36, 36, 36, 36, 36,
               36, 36, 35, 35, 35, 28, 28, 28, 19, 19, 19, 13, 10, 10, 10, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0]
    y_axis = [0, 0, 2, 2, 5, 5, 5, 15, 16, 17, 20, 30, 31, 32, 35, 43, 46, 49, 53, 55, 60, 62, 62, 70, 70, 70, 73, 73,
              72, 72, 72, 72, 70, 70, 70, 70, 72, 72, 72, 72, 72, 72, 73, 73, 71, 71, 71, 71, 58, 58, 50, 50, 39, 39, 25, 25,
              19, 19, 5, 5, 3, 3, 0, 0]

    milliseconds_in_readable_time = []

    for index in range(len(x_axis)):
        if index % 10 == 0:
            milliseconds_in_readable_time.append(convert_millis(x_axis[index]))
        else:
            milliseconds_in_readable_time.append("")

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_axis, y_axis, label='4 CPU\'s (80 Empfänger)')  # Plot some data on the axes.
    ax.plot(x_axis, y_axis3, label='2 CPU\'s (40 Empfänger)')
    ax.plot(x_axis, y_axis2, label='1 CPU\'s (17 Empfänger)')
    fig.set_size_inches(12, 8)
    new_x_axis, new_labels = get_x_axis_with_less_ticks(x_axis, milliseconds_in_readable_time)
    plt.xticks(new_x_axis, new_labels)
    plt.xlabel('Vergangene Zeit in Minuten')
    plt.ylabel('Bandbreite in Mb/s')
    plt.legend()
    plt.savefig('Bandbreite-Ant-Media.png', bbox_inches='tight')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_server_cpu_chart_ant()
    build_server_bandbreite_chart_janus()
    build_server_bandbreite_chart_ant()
    start()

