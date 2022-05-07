from urllib.parse import urljoin
import datetime


class Scraping:
    def __init__(self):
        self.list_campaign_url = []
        self.list_campaign_name = []
        self.list_campaign_fundriser = []
        self.list_campaign_donation = []
        self.list_time = []
        self.list_publisher_name = []
        self.list_update_time = []
        self.list_update_content_h4 = []
        self.list_update_content_p = []
        self.list_update_content_div = []
        self.list_url_scrapping = []
        self.list_donatur = []
        self.list_donasi = []
        self.list_donor_time = []
        self.list_url_donor = []
        self.list_scrap_time = []

    def scrap(self, page_soup):
        # Set empty array
        self.list_campaign_url = []
        self.list_campaign_name = []
        self.list_campaign_fundriser = []
        self.list_campaign_donation = []

        # Get all campaign content card
        campaign_soup = page_soup.find_all("div", class_="m-card")

        # Scrap campaign url
        for x in campaign_soup:
            y = x.find("a")
            z = y["href"]  # Get href inside tag a
            url = urljoin("https:", z)
            self.list_campaign_url.append(url)

        # Scrap campaign name
        for x in campaign_soup:
            campaign_name = x.find("h3")
            self.list_campaign_name.append(campaign_name.text.strip())

        # Scrap campaign fundriser
        for x in campaign_soup:
            campaign_fundriser = x.find("div", class_="m-card__subtitle")
            self.list_campaign_fundriser.append(campaign_fundriser.text.strip())

        # Scrap campaign donation
        for x in campaign_soup:
            campaign_donation = x.find_all("div", class_="m-card__stats")
            for y in campaign_donation:
                x = y.find("span")
                if x.text.strip() == "Terkumpul":
                    z = y.text.replace("Terkumpul", "").replace("Rp", "").replace(".", "").strip()
                    self.list_campaign_donation.append(z)

    def scrap_detail(self, page_soup_detail, url_detail):
        # Set empty array
        self.list_time = []
        self.list_publisher_name = []
        self.list_update_time = []
        self.list_update_content_h4 = []
        self.list_update_content_p = []
        self.list_update_content_div = []
        self.list_url_scrapping = []

        # Content container
        content_soup = page_soup_detail.find_all("div", {"class": "style__TimelineItem-sc-__sc-bl8jwv-3 kGnabC"})
        for x in content_soup:
            reference_time = x.find(class_="style__UpdateTime-sc-__sc-bl8jwv-8 lnbfOR").text
            if "tahun" in reference_time:
                continue

            # Publisher name
            publisher_name = x.find(class_="style__PublisherName-sc-__sc-bl8jwv-7 kiEwbb")
            self.list_publisher_name.append(publisher_name.text.strip())
            self.list_time.append(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            self.list_url_scrapping.append(url_detail)

            # Update time
            update_time = x.find(class_="style__UpdateTime-sc-__sc-bl8jwv-8 lnbfOR")
            self.list_update_time.append(update_time.text.strip())

            # Content donation
            h4_tag = x.find("h4")
            update_content_h4 = h4_tag.text.replace("Pencairan Dana Rp ", ""). \
                replace(".", "").replace("\n", "").replace(",", " ").replace(";", " ").strip()
            self.list_update_content_h4.append(update_content_h4)

            # Content account
            p_tag = x.find("p")
            if "rekening" in p_tag.text:
                update_content_p = p_tag.text.replace("\n", " ").replace("rekening", ""). \
                    replace("ke", "").replace(";", "").strip()
                self.list_update_content_p.append(update_content_p)
            else:
                update_content_p = ""
                self.list_update_content_p.append(update_content_p)

            # Content description
            div_tag = x.find("div")
            update_content_div = div_tag.text.replace("\n", " ").replace(";", ",").strip()
            self.list_update_content_div.append(update_content_div)

    def scrap_donor(self, page_soup_donor, url_donor):
        content_soup = page_soup_donor.find_all("div", {"class": "style__DonorItem-sc-__sc-1exee2-4 fJHQYT"})
        for x in content_soup:
            donatur = x.find(class_="style__DonorName-sc-__sc-1exee2-7 dlOQEY")
            donasi = x.find(class_="style__DonationAmount-sc-__sc-1exee2-8 fCbsWC")
            donor_time = x.find(class_="style__DonationTime-sc-__sc-1exee2-9 kBDzcm")
            self.list_scrap_time.append(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            self.list_donatur.append(donatur.text.strip())
            self.list_donasi.append(donasi.text.replace("Rp", "").replace(".", "").strip())
            self.list_donor_time.append(donor_time.text.strip())
            self.list_url_donor.append(url_donor)
