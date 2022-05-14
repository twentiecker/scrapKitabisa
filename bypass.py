import scrolling

scroll = scrolling.Scrolling()

# url_donor = "https://kitabisa.com/campaign/bwindonesiapastisembuh"
#
# print("===== Start Scrolling Donor Page =====")
# scroll.scroll_donor(url_donor)
# if scroll.validate_url:
#     print("\n===== Finish Scrolling Donor Page =====")
#     print("===== Start Scraping Donor Page =====")
#     # scrap.scrap_donor(scroll.page_soup_donor, url_donor)
#     print("===== Finish Scraping Donor Page =====")
#     print("===== Start Writing Donor Page =====")
#     # write.write_donor(file_name_write_donor, scrap.list_scrap_time, scrap.list_donatur, scrap.list_donasi,
#     #                   scrap.list_donor_time, scrap.list_url_donor)
#     print("===== Finish Writing Donor Page =====")
# else:
#     print("===== Finish Scrolling Donor Page =====")

url_detail = "https://kitabisa.com/campaign/companyforoxyid"

print("===== Start Scrolling Detail Page =====")
scroll.scroll_detail(url_detail)
if scroll.validate_url:
    print("\n===== Finish Scrolling Detail Page =====")
    print("===== Start Scraping Detail Page =====")
    # scrap.scrap_detail(scroll.page_soup_detail, url_detail)
    print("===== Finish Scraping Detail Page =====")
    print("===== Start Writing Detail Page =====")
    # write.write_detail(file_name_write_detail, scrap.list_time, scrap.list_publisher_name,
    #                    scrap.list_update_time, scrap.list_update_content_h4, scrap.list_update_content_p,
    #                    scrap.list_update_content_div, scrap.list_url_scrapping)
    print("===== Finish Writing Detail Page =====")
else:
    print("===== Finish Scrolling Detail Page =====")