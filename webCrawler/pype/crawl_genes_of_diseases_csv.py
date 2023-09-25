# import asyncio
# from pyppeteer import launch
# async def main():
#     browser = await launch(headless=False)
#     page = await browser.newPage()
#     await page.goto('https://www.bilibili.com/v/music/cover?tag=-1')
#     pattern = "a"
#     await page.waitForSelector(pattern, timeout = 30000) # wait up to 30 seconds
#     contents = await page.JJeval(
#         pattern,
#         '(links) => links.map((x) => x.innerText)'
#     )
#     print(contents)
#     await browser.close()

# try:
#     asyncio.get_event_loop().run_until_complete(main())
# except Exception as e:
#     print(f"ERROR!!!!: {e}")





# import asyncio
# from pyppeteer import launch
# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto('https://www.disgenet.org/browser/0/1/0/C0002395/')
#     all_data = []
#     while True:
#         # Step 3: Scrape data from the current page
#         # (assuming data is in a table with id "data-table")
#         page_data = await page.JJeval('a .dsgn-trunc-hidd', 'rows => rows.map(row => row.innerText)')
#         all_data.extend(page_data)
#         breakpoint()
#         # Step 4: Check for a "Next" button and navigate to the next page
#         next_button = await page.querySelector('.fa-chevron-right')
#         if next_button:
#             await next_button.click()
#             await page.waitForNavigation()  # wait for the next page to load
#         else:
#             break  # exit the loop if there's no "Next" button

#     # Step 6: Close the browser
#     await browser.close()

#     print(all_data)  # print or process the scraped data

# asyncio.get_event_loop().run_until_complete(main())






import asyncio
from pyppeteer import launch
import os
import time

async def main():
    download_path = '/Users/a123/proj/genePaper/dsp/jink/'  # Set your download path here

    browser = await launch(  # It's easier to debug in headful mode
        args=[f'--download-path={download_path}']
    )
    page = await browser.newPage()
    await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_path})
    await page.goto('https://www.ncbi.nlm.nih.gov/gene/6622')

    # Click the 'Download Datasets' button
    await page.click('#download-asm > a')
    await page.waitForSelector('#datasets-download-submit > span', timeout=5000)  # Adjust timeout as needed

    # Click the 'Download' button
    await page.click('#datasets-download-submit > span')

    # Wait for download to complete (simple way: sleep for a certain amount of time)
    # A more robust solution would be to check the download directory for the new file
    await asyncio.sleep(10)  # Adjust sleep time as needed

    # Optionally: Check if the download is complete by checking the download directory
    # This is a simplistic check; you might need a more robust solution
    while not any(fname.endswith('.zip') for fname in os.listdir(download_path)):
        print('Waiting for download to complete...')
        breakpoint()
        await asyncio.sleep(2)  # sleep for a bit before checking again

    await browser.close()

    print('Download complete')

asyncio.get_event_loop().run_until_complete(main())














