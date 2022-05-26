import reading
import writing

write = writing.Writing()
read = reading.Reading()

partner_name = "#PerempuanHadapiCovid"

file_name_write_url = f"output/donasi/{partner_name}_url"
file_name_write_url_remainder = f"output/donasi/{partner_name}_remainder"

print("===== Start Reading =====")
write.write_url(file_name_write_url, scrap.list_campaign_url)
print("===== Finish Reading =====")

print("===== Start Writing Url =====")
write.write_url(file_name_write_url, scrap.list_campaign_url)
print("===== Finish Writing Url =====")

# Write remaining url that need to be scraped
print("===== Start Writing Remainder =====")
write.write_url(file_name_write_url_remainder, read.list_url)  # Remainder url
print("===== Finish Writing Remainder =====")

# # Latest-news
# file_name_write_url = f"output/latest-news/{partner_name}_url"
# file_name_write_url_remainder = f"output/latest-news/{partner_name}_remainder"
