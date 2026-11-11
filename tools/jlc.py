"""JLC/LCSC lookup with cache. usage: jlc.py code C123 ... | jlc.py search 'keyword' [n]"""
import json, sys, os, subprocess, time
D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, "jlc_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def curl(args):
    return subprocess.run(["curl", "-s", "-m", "40"] + args, capture_output=True, text=True).stdout

def jlc_search(kw, n=10):
    r = curl(["-X", "POST", "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList",
              "-H", "Content-Type: application/json", "-d", json.dumps({"keyword": kw, "currentPage": 1, "pageSize": n})])
    try:
        return json.loads(r)["data"]["componentPageInfo"]["list"] or []
    except Exception:
        return []

def lcsc(code):
    r = curl([f"https://wmsc.lcsc.com/ftps/wm/product/detail?productCode={code}"])
    try:
        d = json.loads(r)["result"]
    except Exception:
        return {}
    if not d:
        return {}
    return dict(model=d.get("productModel"), brand=d.get("brandNameEn"), lcsc_stock=d.get("stockNumber"),
                pdf=d.get("pdfUrl"), pkg=d.get("encapStandard"),
                params={p.get("paramNameEn"): p.get("paramValueEn") for p in (d.get("paramVOList") or [])})

def info(code, refresh=False):
    if code in cache and not refresh:
        return cache[code]
    lst = [x for x in jlc_search(code, 5) if x["componentCode"] == code]
    out = {"code": code}
    if lst:
        x = lst[0]
        out.update(jlc_type=x["componentLibraryType"], pref=x.get("preferredComponentFlag"), stock=x["stockCount"],
                   prices=[(p["startNumber"], p["productPrice"]) for p in x["componentPrices"]],
                   mfr=x["componentBrandEn"], mpn=x["componentModelEn"], desc=x.get("describe") or x.get("erpComponentName"))
    out.update(lcsc(code))
    cache[code] = out
    json.dump(cache, open(CACHE, "w"), indent=1, ensure_ascii=False)
    time.sleep(0.3)
    return out

def price(code, qty):
    p = info(code).get("prices") or []
    best = None
    for start, pr in sorted(p):
        if qty >= start:
            best = pr
    return best if best is not None else (sorted(p)[0][1] if p else None)

if __name__ == "__main__":
    if sys.argv[1] == "code":
        for c in sys.argv[2:]:
            i = info(c, refresh=True)
            pr = i.get("params", {})
            t = {k: v for k, v in pr.items() if "emp" in k or "Dielectric" in k or "Voltage" in k or "Coefficient" in k}
            print(c, i.get("mfr") or i.get("brand"), i.get("mpn") or i.get("model"), i.get("jlc_type"), "stock", i.get("stock"),
                  "p100", price(c, 100), "p1000", price(c, 1000), t)
    else:
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        for x in jlc_search(sys.argv[2], n):
            print(x["componentCode"], x["componentLibraryType"], x["stockCount"], x["componentBrandEn"], x["componentModelEn"],
                  (x["componentPrices"] or [{}])[0].get("productPrice"), (x.get("describe") or "")[:80])
