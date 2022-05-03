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
            year = int(scrap_date[2])  # year position
            month = int(scrap_date[1])  # month position
            date = int(scrap_date[0])  # date position

            # Determine the quarter
            z = x1[3]  # Get the date of latest-news

            if "hari" in z:
                # Selection for positive value of m_convert
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
                tw1 += int(x1[4])
            elif (m_convert >= 4) and (m_convert <= 6):
                print(f"tw2;{x}")
                tw2 += int(x1[4])
            elif (m_convert >= 7) and (m_convert <= 9):
                print(f"tw3;{x}")
                tw3 += int(x1[4])
            elif (m_convert >= 10) and (m_convert <= 12):
                print(f"tw4;{x}")
                tw4 += int(x1[4])

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
