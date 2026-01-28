(async function() {

  /* -------------------- HELPERS -------------------- */

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function getByXPath(xpath, context = document) {
    return document.evaluate(xpath, context, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  }

  function getAllByXPath(xpath, context = document) {
    const out = [];
    const snap = document.evaluate(xpath, context, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    for (let i = 0; i < snap.snapshotLength; i++) out.push(snap.snapshotItem(i));
    return out;
  }

  function text(xpath) {
    const el = getByXPath(xpath);
    return el ? el.innerText.trim() : "";
  }

  async function waitForJobLoad(timeout = 6000) {
    return new Promise(resolve => {
      const start = Date.now();
      const timer = setInterval(() => {
        const title = text("//h1");
        const company = text("//h2//span");
        if (title || company || Date.now() - start > timeout) {
          clearInterval(timer);
          resolve();
        }
      }, 300);
    });
  }

  function downloadCSV(rows) {
    if (!rows.length) return;
    const headers = Object.keys(rows[0]);
    const csv = [
      headers.join(","),
      ...rows.map(r => headers.map(h => `"${(r[h]||"").replace(/"/g,'""')}"`).join(","))
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `jobs_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    console.log(`📥 CSV downloaded (${rows.length} jobs)`);
  }

  /* -------------------- COMPANY DETAILS -------------------- */

  async function extractCompanyDetails(retries = 3) {
    for(let attempt=0; attempt<retries; attempt++){
      const root = document.querySelector("#company");
      if(!root){ await sleep(500); continue; }

      const textFn = (sel, ctx=root) => ctx.querySelector(sel)?.innerText.trim()||"";

      const CompanyName = textFn(".index_companyName__gsqmt");
      const Summary = textFn(".index_companySummary__IvVpZ");

      let Founded="", CompanySize="", Location="", Website="";
      root.querySelectorAll(".index_company-metadata-item__LgU5Q").forEach(item=>{
        const t = item.innerText.trim();
        if(t.includes("Founded")) Founded=t;
        if(t.includes("employees")) CompanySize=t;
      });

      Location = root.querySelector('img[alt="location"]')?.parentElement.querySelector("div")?.innerText.trim()||"";
      Website = root.querySelector('img[alt="web-link"]')?.parentElement.querySelector("a")?.href||"";

      let Linkedin="", Twitter="", Crunchbase="";
      root.querySelectorAll('a[target="_blank"]').forEach(a=>{
        const h=a.href.toLowerCase();
        if(h.includes("linkedin.com/company")) Linkedin=a.href;
        if(h.includes("x.com")) Twitter=a.href;
        if(h.includes("crunchbase.com")) Crunchbase=a.href;
      });

      const FundingStage = textFn(".index_funding-text__OBvD8");

      const leaders = [...root.querySelectorAll(".index_leadershipBlocksItem__UgBoX")];

      const leader1 = leaders[0] || null;
      const leader2 = leaders[1] || null;

      const Leader1Name = leader1?.querySelector?.(".index_leaderName__T6IuS")?.innerText.trim() || "";
      const Leader1Title = leader1?.querySelector?.(".index_leaderTitle__H5JeW")?.innerText.trim() || "";
      const Leader1Linkedin = leader1?.querySelector?.("a[href*='linkedin.com']")?.href || "";

      const Leader2Name = leader2?.querySelector?.(".index_leaderName__T6IuS")?.innerText.trim() || "";
      const Leader2Title = leader2?.querySelector?.(".index_leaderTitle__H5JeW")?.innerText.trim() || "";
      const Leader2Linkedin = leader2?.querySelector?.("a[href*='linkedin.com']")?.href || "";

      return {
        CompanyName, Founded, Location, CompanySize, Website,
        Linkedin, Twitter, Crunchbase, FundingStage,
        Leader1Name, Leader1Title, Leader1Linkedin,
        Leader2Name, Leader2Title, Leader2Linkedin
      };
    }
    return {}; // fallback empty if retries fail
  }

  /* -------------------- MAIN LOGIC -------------------- */

  const scrollableDiv = document.getElementById("scrollableDiv");
  if(!scrollableDiv){console.error("❌ scrollableDiv not found"); return;}

  let results=[], processedTitles=new Set();
  let idleScrolls=0;

  while(idleScrolls < 3){

    // Re-query clickable divs each loop to get newly loaded jobs
    const clickableDivs = getAllByXPath("//div[2]/div[2]/div[4]/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div[2]");

    let newJobsFound = false;

    for(const div of clickableDivs){
      if(!div || !div.isConnected) continue;

      div.scrollIntoView({block:"center", behavior:"smooth"});
      await sleep(400);
      div.click();
      await waitForJobLoad();
      await sleep(700);

      const jobTitle = text("//h1");
      if(!jobTitle || processedTitles.has(jobTitle)) continue;

      newJobsFound = true;

      // JOB DATA
      const jobData = {
        JobTitle: jobTitle,
        JobCompanyName: text("//h2//span"),
        Country: text("//span[contains(text(),'United')]"),
        JobType: text("//span[contains(text(),'Remote')]")
      };

      // COMPANY DATA
      const companyData = await extractCompanyDetails();
      const data = {...jobData, ...companyData};

      processedTitles.add(jobTitle);
      results.push(data);

      console.log(`✅ Job ${results.length}`, data);

      // Close job detail
      getByXPath("//button[@aria-label='Close']")?.click();

      // Download every 10 jobs
      if(results.length % 10 === 0){
        downloadCSV(results.splice(0, results.length));
      }

      await sleep(500);
    }

    // Scroll to load more jobs
    const oldHeight = scrollableDiv.scrollHeight;
    scrollableDiv.scrollTop = oldHeight;
    await sleep(4000);

    if(!newJobsFound && scrollableDiv.scrollHeight === oldHeight){
      idleScrolls++;
      console.log(`⚠️ No new jobs loaded (${idleScrolls}/3)`);
    }else{
      idleScrolls=0;
    }
  }

  // Final download
  if(results.length) downloadCSV(results);

  console.log("🏁 DONE — all jobs processed");

})();
