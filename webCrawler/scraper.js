const puppeteer = require("puppeteer");

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    await page.goto("https://www.bilibili.com/v/music/cover?tag=-1");

    await page.$$eval(".vd-list-cnt > ul > li > div > div.r > a", (results) => {
        results.map((result) => result.innerText);
    }
    );
})();