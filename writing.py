class Writing:
    def write(self, file_name, list_campaign_name, list_campaign_fundriser, list_campaign_donation, list_campaign_url):
        f = open(f"{file_name}.csv", "a+", encoding="utf-8")  # open/create file and then append some item (a+)
        for i in range(len(list_campaign_name)):
            f.write(
                f"{list_campaign_name[i]};{list_campaign_fundriser[i]};{list_campaign_donation[i]};{list_campaign_url[i]}\n")
        f.close()

    def write_url(self, file_name, list_campaign_url):
        f = open(f"{file_name}.csv", "w+", encoding="utf-8")  # create/overwrite file (w+)
        for i in range(len(list_campaign_url)):
            f.write(f"{list_campaign_url[i]}\n")
        f.close()

    def write_detail(self, file_name, list_time, list_publisher_name, list_update_time, list_update_content_h4,
                     list_update_content_p, list_update_content_div, list_url_scrapping):
        f = open(f"{file_name}.csv", "a+", encoding="utf-8")  # open/create file and then append some item (a+)
        for i in range(len(list_time)):
            f.write(
                f"{list_time[i]};{list_publisher_name[i]};{list_update_time[i]};{list_update_content_h4[i]};{list_update_content_p[i]};{list_update_content_div[i]};{list_url_scrapping[i]}\n")
        f.close()

    def write_summary(self, file_name, list_summary):
        f = open(f"{file_name}.csv", "w+", encoding="utf-8")  # open/create file and then append some item (a+)
        for i in range(len(list_summary)):
            f.write(f"{list_summary[i]}\n")
        f.close()
