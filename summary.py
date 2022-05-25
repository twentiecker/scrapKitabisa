from dask import dataframe as dd
import reading
import writing


class Summary:
    def summary(self, file_name):
        read = reading.Reading()
        write = writing.Writing()

        read.read_detail(file_name)
        rows = read.list_detail

        list_summary = []
        tw1 = 0
        tw2 = 0
        tw3 = 0
        tw4 = 0
        m_convert = 0
        for x in rows:
            x1 = x.split(";")

            # Get scraping month
            y = x.split(";")
            scrap_date = y[0].split("/")  # split date, month, and year in form of array
            year = int(((scrap_date[2]).split(","))[0])  # year position
            month = int(scrap_date[1])  # month position
            date = int(scrap_date[0])  # date position

            # Determine the quarter
            z = x1[2]  # Get the date of latest-news

            if "hari" in z:
                # Selection for positive value of m_convert
                if "sehari" in z:
                    m_convert = date - 1
                else:
                    m_convert = date - int(z.split()[0])

                if m_convert < 0:
                    m_convert = month - 1
                else:
                    m_convert = month
            elif "bulan" in z:
                if z == "sebulan yang lalu":
                    m_convert = month - 1
                else:
                    m_convert = month - int(z.split()[0])
                    if m_convert < 1:
                        m_convert += 12

            if (m_convert >= 1) and (m_convert <= 3):
                print(f"tw1;{x}")
                tw1 += int(x1[3])
            elif (m_convert >= 4) and (m_convert <= 6):
                print(f"tw2;{x}")
                tw2 += int(x1[3])
            elif (m_convert >= 7) and (m_convert <= 9):
                print(f"tw3;{x}")
                tw3 += int(x1[3])
            elif (m_convert >= 10) and (m_convert <= 12):
                print(f"tw4;{x}")
                tw4 += int(x1[3])

        if (month >= 1) and (month <= 3):
            list_summary.append(f"Triwulan I {year};{tw1}")
            list_summary.append(f"Triwulan IV {year - 1};{tw4}")
            list_summary.append(f"Triwulan III {year - 1};{tw3}")
            list_summary.append(f"Triwulan II {year - 1};{tw2}")
        elif (month >= 4) and (month <= 6):
            list_summary.append(f"Triwulan II {year};{tw2}")
            list_summary.append(f"Triwulan I {year};{tw1}")
            list_summary.append(f"Triwulan IV {year - 1};{tw4}")
            list_summary.append(f"Triwulan III {year - 1};{tw3}")
        elif (month >= 7) and (month <= 9):
            list_summary.append(f"Triwulan III {year};{tw3}")
            list_summary.append(f"Triwulan II {year};{tw2}")
            list_summary.append(f"Triwulan I {year};{tw1}")
            list_summary.append(f"Triwulan IV {year - 1};{tw4}")
        elif (month >= 10) and (month <= 12):
            list_summary.append(f"Triwulan IV {year};{tw4}")
            list_summary.append(f"Triwulan III {year};{tw3}")
            list_summary.append(f"Triwulan II {year};{tw2}")
            list_summary.append(f"Triwulan I {year};{tw1}")

        file_name = file_name.replace("detail", "summary")
        write.write_summary(file_name, list_summary)

    def summary_donor(self, file_name):
        write = writing.Writing()
        df = dd.read_csv(f"{file_name}.csv", sep=";", header=None, on_bad_lines='skip')

        tw1 = 0
        tw2 = 0
        tw3 = 0
        tw4 = 0

        i = 0
        while True:
            try:
                df_rows = df.partitions[i].compute().values
                rows = df_rows.tolist()  # convert numpy array to normal array
                # scrap_date = rows[0][0]  # scrap_date
                # anchor_month = scrap_date.split(sep="/")[1]
                # anchor_date = scrap_date.split(sep="/")[2]
                # anchor_year = int(anchor_date.split(sep=",")[0])

                quarter_dic = {"Januari": 1, "Februari": 1, "Maret": 1, "April": 2, "Mei": 2, "Juni": 2, "Juli": 3,
                               "Agustus": 3, "September": 3, "Oktober": 4, "November": 4, "Desember": 4}

                quarter_anchor_dic = {"01": 1, "02": 1, "03": 1, "04": 2, "05": 2, "06": 2, "07": 3, "08": 3, "09": 3,
                                      "10": 4, "11": 4, "12": 4}

                list_summary = []
                for x in rows:
                    scrap_date = x[0]
                    # print(scrap_date)
                    anchor_month = scrap_date.split(sep="/")[1]
                    anchor_date = scrap_date.split(sep="/")[2]
                    anchor_year = int(anchor_date.split(sep=",")[0])

                    row_date = x[3].split(sep=" ")  # Get date
                    row_month = row_date[1]  # Get month
                    row_year = int(row_date[2])  # Get year

                    # Filter for below the quarter anchor
                    if quarter_dic[row_month] <= quarter_anchor_dic[anchor_month] and row_year <= anchor_year - 1:
                        continue

                    # Filter for above the quarter anchor
                    if quarter_dic[row_month] > quarter_anchor_dic[anchor_month] and row_year < anchor_year - 1:
                        continue

                    row_donasi = x[2]

                    if quarter_dic[row_month] == 1:
                        x.insert(0, f"tw{quarter_dic[row_month]}")
                        print(x)
                        tw1 += int(row_donasi)
                    elif quarter_dic[row_month] == 2:
                        x.insert(0, f"tw{quarter_dic[row_month]}")
                        print(x)
                        tw2 += int(row_donasi)
                    elif quarter_dic[row_month] == 3:
                        x.insert(0, f"tw{quarter_dic[row_month]}")
                        print(x)
                        tw3 += int(row_donasi)
                    elif quarter_dic[row_month] == 4:
                        x.insert(0, f"tw{quarter_dic[row_month]}")
                        print(x)
                        tw4 += int(row_donasi)

                i += 1
            except IndexError:
                break

        if (int(anchor_month) >= 1) and (int(anchor_month) <= 3):
            list_summary.append(f"Triwulan I {anchor_year};{tw1}")
            list_summary.append(f"Triwulan IV {anchor_year - 1};{tw4}")
            list_summary.append(f"Triwulan III {anchor_year - 1};{tw3}")
            list_summary.append(f"Triwulan II {anchor_year - 1};{tw2}")
        elif (int(anchor_month) >= 4) and (int(anchor_month) <= 6):
            list_summary.append(f"Triwulan II {anchor_year};{tw2}")
            list_summary.append(f"Triwulan I {anchor_year};{tw1}")
            list_summary.append(f"Triwulan IV {anchor_year - 1};{tw4}")
            list_summary.append(f"Triwulan III {anchor_year - 1};{tw3}")
        elif (int(anchor_month) >= 7) and (int(anchor_month) <= 9):
            list_summary.append(f"Triwulan III {anchor_year};{tw3}")
            list_summary.append(f"Triwulan II {anchor_year};{tw2}")
            list_summary.append(f"Triwulan I {anchor_year};{tw1}")
            list_summary.append(f"Triwulan IV {anchor_year - 1};{tw4}")
        elif (int(anchor_month) >= 10) and (int(anchor_month) <= 12):
            list_summary.append(f"Triwulan IV {anchor_year};{tw4}")
            list_summary.append(f"Triwulan III {anchor_year};{tw3}")
            list_summary.append(f"Triwulan II {anchor_year};{tw2}")
            list_summary.append(f"Triwulan I {anchor_year};{tw1}")

        file_name = file_name.replace("donor", "summary")
        write.write_summary(file_name, list_summary)
