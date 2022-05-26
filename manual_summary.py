# import summary
#
# file_name = "output/donasi/Oxygen for Indonesia_donor"
# summ = summary.Summary()
# summ.summary_donor(file_name)

import sys
import time

for i in range(10):
    sys.stdout.write(f"\r===== Scrolling count: {i} ({i+2} days) =====")
    sys.stdout.flush()
    if i == 9:
        sys.stdout.write(f"\nend")
        sys.stdout.flush()
        break
    if i == 2:
        print("\nbaris 2")
    time.sleep(1)
print("\nbaris terakhir")