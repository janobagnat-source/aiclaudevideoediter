"""Búsqueda y descarga de assets gratuitos con licencia registrada (créditos en credits.json).

Tipos y proveedores (en orden de preferencia; los que requieren key se saltan si no hay key):
  video    pexels(PEXELS_API_KEY) · pixabay(PIXABAY_API_KEY)
  photo    pexels · pixabay · unsplash(UNSPLASH_ACCESS_KEY) · openverse(sin key)
  music    jamendo(JAMENDO_CLIENT_ID) · openverse(sin key, Jamendo/ccMixter CC-BY/CC0) · freesound
  sfx      bigsoundbank(sin key, CC0) · freesound(FREESOUND_API_KEY) · openverse(Freesound CC0; la CDN de
           Freesound puede bloquear IPs de nube) · + packs Kenney CC0 en `ve library build`
  3d       polyhaven(sin key, CC0 glTF) · sketchfab(SKETCHFAB_API_TOKEN, descargables CC)
  hdri     polyhaven        texture  polyhaven
  icon     iconify(sin key, SVG de +150 sets open source)

Ejemplos:
  ve stock video "business meeting" --orientation portrait -n 4 -p cliente/proyecto
  ve stock sfx "whoosh" -n 6
  ve stock music "epic cinematic trailer" -n 5
  ve stock 3d "camera" -n 3
  ve stock icon "rocket"
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
from pathlib import Path

import requests

from vecommon import LIBRARY, add_credit, env, log, resolve_project, run, work_dir, write_json

UA = {"User-Agent": "ve-video-editor/1.0"}
TIMEOUT = 40
COMMERCIAL_OK = {"cc0", "pdm", "by", "by-sa", "pexels", "pixabay", "unsplash", "polyhaven", "iconify"}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50]


def download(url: str, dst: Path, headers: dict | None = None) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    with requests.get(url, headers={**UA, **(headers or {})}, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with open(dst, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return dst


def gj(url: str, headers: dict | None = None, params: dict | None = None) -> dict:
    r = requests.get(url, headers={**UA, **(headers or {})}, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------- VIDEO / PHOTO
def pexels_video(q, n, orientation, **_):
    key = env("PEXELS_API_KEY")
    if not key:
        return None
    d = gj("https://api.pexels.com/videos/search", {"Authorization": key},
           {"query": q, "per_page": n, "orientation": orientation or "", "size": "large"})
    out = []
    for v in d.get("videos", []):
        files = sorted([f for f in v["video_files"] if f.get("file_type") == "video/mp4" and f.get("height")],
                       key=lambda f: f["height"] * f["width"], reverse=True)
        best = next((f for f in files if max(f["width"], f["height"]) <= 3840), files[0] if files else None)
        if best:
            out.append({"id": f"pexels-{v['id']}", "url": best["link"], "ext": ".mp4", "w": best["width"],
                        "h": best["height"], "duration": v.get("duration"), "page": v["url"],
                        "author": v.get("user", {}).get("name"), "license": "pexels"})
    return out


def pixabay_video(q, n, orientation, **_):
    key = env("PIXABAY_API_KEY")
    if not key:
        return None
    d = gj("https://pixabay.com/api/videos/", params={"key": key, "q": q, "per_page": max(3, n), "safesearch": "true"})
    out = []
    for v in d.get("hits", [])[:n]:
        vs = v["videos"]
        best = vs.get("large") if vs.get("large", {}).get("url") else vs.get("medium")
        out.append({"id": f"pixabay-{v['id']}", "url": best["url"], "ext": ".mp4", "w": best["width"],
                    "h": best["height"], "duration": v.get("duration"), "page": v["pageURL"],
                    "author": v.get("user"), "license": "pixabay"})
    if orientation == "portrait":
        out.sort(key=lambda x: x["h"] < x["w"])
    return out


def pexels_photo(q, n, orientation, **_):
    key = env("PEXELS_API_KEY")
    if not key:
        return None
    d = gj("https://api.pexels.com/v1/search", {"Authorization": key},
           {"query": q, "per_page": n, "orientation": orientation or ""})
    return [{"id": f"pexels-{p['id']}", "url": p["src"]["original"], "ext": ".jpg", "w": p["width"], "h": p["height"],
             "page": p["url"], "author": p.get("photographer"), "license": "pexels"} for p in d.get("photos", [])]


def pixabay_photo(q, n, orientation, **_):
    key = env("PIXABAY_API_KEY")
    if not key:
        return None
    d = gj("https://pixabay.com/api/", params={"key": key, "q": q, "per_page": max(3, n), "image_type": "photo",
                                                 "orientation": {"portrait": "vertical", "landscape": "horizontal"}.get(orientation or "", "all")})
    return [{"id": f"pixabay-{p['id']}", "url": p.get("largeImageURL"), "ext": ".jpg", "w": p["imageWidth"],
             "h": p["imageHeight"], "page": p["pageURL"], "author": p.get("user"), "license": "pixabay"}
            for p in d.get("hits", [])[:n]]


def unsplash_photo(q, n, orientation, **_):
    key = env("UNSPLASH_ACCESS_KEY")
    if not key:
        return None
    d = gj("https://api.unsplash.com/search/photos", {"Authorization": f"Client-ID {key}"},
           {"query": q, "per_page": n, **({"orientation": orientation} if orientation else {})})
    return [{"id": f"unsplash-{p['id']}", "url": p["urls"]["full"], "ext": ".jpg", "w": p["width"], "h": p["height"],
             "page": p["links"]["html"], "author": p["user"]["name"], "license": "unsplash"} for p in d.get("results", [])]


def openverse_photo(q, n, orientation, **_):
    params = {"q": q, "page_size": n, "license_type": "commercial,modification", "mature": "false"}
    if orientation:
        params["aspect_ratio"] = {"portrait": "tall", "landscape": "wide", "square": "square"}[orientation]
    d = gj("https://api.openverse.org/v1/images/", params=params)
    return [{"id": f"ov-{r['id'][:12]}", "url": r["url"], "ext": Path(urllib.parse.urlparse(r["url"]).path).suffix or ".jpg",
             "w": r.get("width"), "h": r.get("height"), "page": r.get("foreign_landing_url"), "author": r.get("creator"),
             "license": r["license"], "attribution": r.get("attribution")} for r in d.get("results", [])]


# ---------------------------------------------------------------- AUDIO
def openverse_audio(q, n, kind, **_):
    words = q.split()
    results = []
    for k in range(len(words), 0, -1):  # si la búsqueda exacta no da resultados, se va relajando
        params = {"q": " ".join(words[:k]), "page_size": max(20, n * 3), "license_type": "commercial,modification"}
        if kind == "sfx":
            params.update({"source": "freesound", "license": "cc0"})
        else:
            params["category"] = "music"
        results = gj("https://api.openverse.org/v1/audio/", params=params).get("results", [])
        if len(results) >= n:
            break
    out = []
    for r in results:
        if r["license"] not in COMMERCIAL_OK:
            continue
        dur = (r.get("duration") or 0) / 1000
        if kind == "sfx" and dur > 12:
            continue
        if kind == "music" and dur and dur < 30:
            continue
        ext = ".mp3" if (r.get("filetype") in (None, "mp3", "mp32")) else f".{r['filetype']}"
        out.append({"id": f"ov-{r['id'][:12]}", "url": r["url"], "ext": ext, "duration": dur, "page": r.get("foreign_landing_url"),
                    "author": r.get("creator"), "license": r["license"], "title": r.get("title"),
                    "attribution": r.get("attribution"), "provider": r.get("provider")})
    return out[:n]


def freesound(q, n, kind, **_):
    key = env("FREESOUND_API_KEY")
    if not key:
        return None
    flt = "duration:[0 TO 12]" if kind == "sfx" else "duration:[30 TO 600]"
    d = gj("https://freesound.org/apiv2/search/text/", params={
        "query": q, "token": key, "page_size": n, "sort": "rating_desc",
        "filter": f'{flt} license:("Creative Commons 0" OR "Attribution")',
        "fields": "id,name,previews,license,username,url,duration,avg_rating"})
    out = []
    for r in d.get("results", []):
        lic = "cc0" if "zero" in r["license"].lower() or "publicdomain" in r["license"] else "by"
        out.append({"id": f"fs-{r['id']}", "url": r["previews"]["preview-hq-mp3"], "ext": ".mp3", "duration": r["duration"],
                    "page": r["url"], "author": r["username"], "license": lic, "title": r["name"]})
    return out


def bigsoundbank(q, n, kind, **_):
    """BigSoundBank.com: +3500 SFX, se verifica que cada sonido sea CC0 en su página."""
    if kind != "sfx":
        return None
    r = requests.get("https://bigsoundbank.com/search", params={"q": q}, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    hits = re.findall(r"<a href='/([a-z0-9-]+-s(\d+)\.html)'>([^<]+)<", r.text)
    out, seen = [], set()
    for slug_, sid, title in hits:
        if sid in seen:
            continue
        seen.add(sid)
        if len(out) >= n:
            break
        page = f"https://bigsoundbank.com/{slug_}"
        try:
            html = requests.get(page, headers=UA, timeout=TIMEOUT).text
        except Exception:
            continue
        if "CC0 (public domain)" not in html:
            continue
        out.append({"id": f"bsb-{sid}", "url": f"https://bigsoundbank.com/UPLOAD/mp3/{sid}.mp3", "ext": ".mp3",
                    "page": page, "author": "Joseph Sardin (BigSoundBank)", "license": "cc0", "title": title.strip()})
    return out


def jamendo(q, n, kind, **_):
    cid = env("JAMENDO_CLIENT_ID")
    if not cid or kind != "music":
        return None
    d = gj("https://api.jamendo.com/v3.0/tracks/", params={
        "client_id": cid, "format": "json", "limit": n, "search": q, "audioformat": "mp32",
        "include": "licenses musicinfo", "order": "popularity_total", "ccsa": "false", "ccnd": "false"})
    out = []
    for r in d.get("results", []):
        lic = r.get("license_ccurl", "")
        if "-nc" in lic or "-nd" in lic:
            continue
        out.append({"id": f"jam-{r['id']}", "url": r["audio"], "ext": ".mp3", "duration": r["duration"],
                    "page": r["shareurl"], "author": r["artist_name"], "license": "by" if "/by/" in lic else lic,
                    "title": r["name"]})
    return out


# ---------------------------------------------------------------- 3D / HDRI / TEXTURES / ICONS
def polyhaven(q, n, kind, res="2k", **_):
    t = {"3d": "models", "hdri": "hdris", "texture": "textures"}[kind]
    assets = gj("https://api.polyhaven.com/assets", params={"t": t})
    ql = q.lower().split()
    scored = []
    for aid, meta in assets.items():
        hay = " ".join([aid, meta.get("name", "")] + meta.get("tags", []) + meta.get("categories", [])).lower()
        s = sum(1 for w in ql if w in hay)
        if s:
            scored.append((s, meta.get("download_count", 0), aid, meta))
    scored.sort(reverse=True)
    out = []
    for _, _, aid, meta in scored[:n]:
        files = gj(f"https://api.polyhaven.com/files/{aid}")
        if kind == "3d":
            g = files["gltf"].get(res) or files["gltf"].get("1k") or next(iter(files["gltf"].values()))
            g = g["gltf"]
            out.append({"id": f"ph-{aid}", "url": g["url"], "ext": ".gltf", "include": g.get("include", {}),
                        "page": f"https://polyhaven.com/a/{aid}", "author": ", ".join(meta.get("authors", {})),
                        "license": "cc0", "title": meta.get("name")})
        elif kind == "hdri":
            h = files["hdri"].get(res) or files["hdri"]["1k"]
            out.append({"id": f"ph-{aid}", "url": h["hdr"]["url"], "ext": ".hdr", "page": f"https://polyhaven.com/a/{aid}",
                        "author": ", ".join(meta.get("authors", {})), "license": "cc0", "title": meta.get("name")})
        else:
            diff = files.get("Diffuse", {}).get(res, {}).get("jpg") or files.get("Diffuse", {}).get("1k", {}).get("jpg")
            if diff:
                out.append({"id": f"ph-{aid}", "url": diff["url"], "ext": ".jpg", "page": f"https://polyhaven.com/a/{aid}",
                            "author": ", ".join(meta.get("authors", {})), "license": "cc0", "title": meta.get("name")})
    return out


def sketchfab(q, n, kind, **_):
    tok = env("SKETCHFAB_API_TOKEN")
    if not tok or kind != "3d":
        return None
    d = gj("https://api.sketchfab.com/v3/search", params={"type": "models", "q": q, "downloadable": "true",
                                                         "count": n * 2, "sort_by": "-likeCount"})
    out = []
    for m in d.get("results", []):
        lic = (m.get("license") or {}).get("slug", "")
        if lic not in ("cc0", "by", "by-sa"):
            continue
        try:
            dl = gj(f"https://api.sketchfab.com/v3/models/{m['uid']}/download", {"Authorization": f"Token {tok}"})
        except Exception:
            continue
        g = dl.get("glb") or dl.get("gltf")
        if not g:
            continue
        out.append({"id": f"sf-{m['uid'][:10]}", "url": g["url"], "ext": ".glb" if "glb" in dl else ".zip",
                    "page": m["viewerUrl"], "author": m["user"]["displayName"], "license": lic, "title": m["name"]})
        if len(out) >= n:
            break
    return out


def iconify(q, n, **_):
    d = gj("https://api.iconify.design/search", params={"query": q, "limit": max(n, 32)})
    out = []
    pref = ("ph", "solar", "tabler", "lucide", "mdi", "fluent", "material-symbols", "streamline", "fluent-emoji-flat", "noto")
    icons = sorted(d.get("icons", []), key=lambda x: next((i for i, p in enumerate(pref) if x.startswith(p + ":")), 99))
    for ic in icons[:n]:
        prefix, name = ic.split(":")
        out.append({"id": f"icon-{prefix}-{name}", "url": f"https://api.iconify.design/{prefix}/{name}.svg",
                    "ext": ".svg", "page": f"https://icon-sets.iconify.design/{prefix}/{name}/",
                    "license": "iconify", "author": prefix, "title": ic})
    return out


PROVIDERS = {
    "video": [pexels_video, pixabay_video],
    "photo": [pexels_photo, pixabay_photo, unsplash_photo, openverse_photo],
    "music": [jamendo, openverse_audio, freesound],
    "sfx": [bigsoundbank, freesound, openverse_audio],
    "3d": [polyhaven, sketchfab],
    "hdri": [polyhaven],
    "texture": [polyhaven],
    "icon": [iconify],
}


def search(kind: str, q: str, n: int = 5, orientation: str | None = None, provider: str | None = None) -> list[dict]:
    results: list[dict] = []
    for fn in PROVIDERS[kind]:
        if provider and provider not in fn.__name__:
            continue
        try:
            r = fn(q=q, n=n, kind=kind, orientation=orientation)
        except Exception as e:  # un proveedor caído no frena la búsqueda
            log(f"{fn.__name__}: {e}")
            continue
        if r is None:
            log(f"{fn.__name__}: sin API key, salto")
            continue
        results.extend(r)
        if len(results) >= n:
            break
    return results[:n]


def fetch(item: dict, kind: str, dest_root: Path, project: Path | None, query: str) -> Path:
    d = dest_root / kind / slug(query)
    local = d / f"{item['id']}{item['ext']}"
    download(item["url"], local)
    for rel, inc in (item.get("include") or {}).items():  # texturas/bin de un glTF
        download(inc["url"], d / rel)
    if kind == "video":
        sheet = local.with_suffix(".sheet.jpg")
        if not sheet.exists():
            run(["ffmpeg", "-v", "error", "-y", "-i", local, "-vf",
                 "fps=1,scale=240:-2,tile=6x2:padding=2", "-frames:v", "1", sheet], check=False)
        item["sheet"] = str(sheet)
    add_credit(project, {"local": str(local), "kind": kind, "query": query, "title": item.get("title"),
                         "author": item.get("author"), "license": item.get("license"), "page": item.get("page"),
                         "attribution": item.get("attribution")})
    item["local"] = str(local)
    return local


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=list(PROVIDERS))
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("-p", "--project", help="cliente/proyecto: guarda en _work/assets y registra créditos ahí")
    ap.add_argument("--orientation", choices=["portrait", "landscape", "square"])
    ap.add_argument("--provider")
    ap.add_argument("--list", action="store_true", help="solo listar, no descargar")
    a = ap.parse_args(argv)
    proj = resolve_project(a.project) if a.project else None
    dest = (work_dir(proj) / "assets") if proj else LIBRARY
    res = search(a.kind, a.query, a.n, a.orientation, a.provider)
    if not res:
        raise SystemExit("Sin resultados (¿faltan API keys? ver README → API keys)")
    for it in res:
        if not a.list:
            try:
                fetch(it, a.kind, dest, proj, a.query)
            except Exception as e:
                log(f"descarga fallida {it['id']}: {e}")
                continue
        it.pop("include", None)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
