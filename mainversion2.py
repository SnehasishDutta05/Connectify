import csv
import datetime
import tkinter as tk





def get_todays_date():
    # Get today's date
    today = datetime.date.today()
    return today
def compare_dates(date1, date2):
    # Convert strings to datetime.date objects if necessary
    if isinstance(date1, str):
        date1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    if isinstance(date2, str):
        date2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
    if date1 < date2:
        return 1
    else:
        return 0
def fetch_data(keyword):

    # Twitte, Meta  has blocked all the scrappers and API for scrapping data
    with open('dates.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        date = get_todays_date()
        writer.writerow([date, keyword])
    pass
def take_decision(keyword):
    filename = "dates.csv"
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            last_row = None
            for row in reader:
                last_row = row
        todays_date = str(get_todays_date())

        comparison = compare_dates(last_row[0], todays_date)
        if comparison:
            fetch_data(keyword)
            print(("loading latest data...."))
        else:
            rows_with_date = []
            with open('dates.csv', 'r', newline='') as file:
                reader = csv.reader(file)

                for row in reader:

                    if row[0] == todays_date:
                        rows_with_date.append(row)
            flag = 0
            for i in rows_with_date:
                if i[1] == keyword:
                    flag = 1
            if (flag == 0):
                fetch_data(keyword)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")
def fetch_data_from_file(filename,keyword):
    try:
        data = []
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row and row[0] == keyword:  # Check if the first column is 'Technology'
                    data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
def calculate_percentile(all_scores, given_score):
    less_than_or_equal = sum(score <= given_score for score in all_scores)
    percentile = (less_than_or_equal / len(all_scores)) * 100
    return percentile
def socring(keyword):
    filename = 'demo.csv'

    data = fetch_data_from_file(filename,keyword)

    templikes = [sublist[4] for sublist in data]
    likes = [int(value) for value in templikes]
    tempshares = [sublist[5] for sublist in data]
    shares = [int(value) for value in tempshares]
    tempcomments = [sublist[6] for sublist in data]
    comments = [int(value) for value in tempcomments]
    tempviews = [sublist[7] for sublist in data]
    views = [int(value) for value in tempviews]

    for row in data:
        score = 0

        percentile = calculate_percentile(likes,int(row[4]))
        score += percentile

        percentile = calculate_percentile(shares, int(row[5]))
        score += percentile

        percentile = calculate_percentile(comments, int(row[6]))
        score += percentile

        percentile = calculate_percentile(views, int(row[7]))
        score += percentile

        row.append(score)

    return data
def updates(scored_data,n):
    sorted_data = sorted(scored_data, key=lambda x: x[-1], reverse=True)
    top_data = sorted_data[:n]

    return top_data


def main():
    keyword = keyword_entry.get()
    num_updates = int(num_updates_entry.get())

    take_decision(keyword)
    scored_data = socring(keyword)
    top_data = updates(scored_data,num_updates)

    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)

    for item in top_data:
        post = item[9]
        name = item[2]
        hashtag = item[8]

        output_text.insert(tk.END, f"@{name} : \n")
        output_text.insert(tk.END, f"{post}\n")
        output_text.insert(tk.END, f"{hashtag}\n")


        output_text.insert(tk.END, f"\n")

        # print(item)
    output_text.config(state=tk.DISABLED)
    output_text.config(height=50, width=50)


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Connectify")
    font_style = ("Helvetica", 18)

    # Define the font style for the labels
    label_font = ("Arial", 12, "bold")
    label_font2 = ("Comic Sans MS", 30, "bold")


    # Create the top bar frame with background color
    top_bar_frame = tk.Frame(root, bg='black')
    top_bar_frame.pack(side=tk.TOP, fill=tk.X)

    # Create and pack the profile label with the specified font
    profile_label = tk.Label(top_bar_frame, text="Profile", bg='black', fg='white', font=label_font)
    profile_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Create and pack the connectify label with the specified font
    connectify_label = tk.Label(top_bar_frame, text="Connectify", bg='black', fg='white', font=label_font2)
    connectify_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)

    # Create and pack the settings label with the specified font
    settings_label = tk.Label(top_bar_frame, text="Settings", bg='black', fg='white', font=label_font)
    settings_label.pack(side=tk.RIGHT, padx=10, pady=10)

    frame2 = tk.Frame(root)
    frame2.pack(side=tk.TOP, fill=tk.X)

    # Create and pack the widgets
    keyword_label = tk.Label(frame2, text="Search:", font=font_style)
    keyword_label.pack(side=tk.LEFT, padx=10, pady=10)

    keyword_entry = tk.Entry(frame2)
    keyword_entry.pack(side=tk.RIGHT, padx=10, pady=10)

    frame3 = tk.Frame(root)
    frame3.pack(side=tk.TOP, fill=tk.X)

    num_updates_label = tk.Label(frame3, text="Enter number of updates:" , font=font_style)
    num_updates_label.pack(side=tk.LEFT, padx=10, pady=10)

    num_updates_entry = tk.Entry(frame3)
    num_updates_entry.pack(side=tk.RIGHT, padx=10, pady=10)

    frame4 = tk.Frame(root, pady=10)
    frame4.pack(side=tk.TOP, fill=tk.X)

    display_button = tk.Button(frame4, text="SEARCH", command=main)
    display_button.pack()


    # Create the output text widget with horizontal fill
    output_text = tk.Text(root, height=50, width= 50, state=tk.DISABLED , font=font_style)
    output_text.pack(fill=tk.X)

    root.mainloop()
