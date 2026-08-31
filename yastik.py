#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T.C. İskân Genel Müdürlüğü — Yastık Göç Kayıt Yazılımı

Gerçekten çalışır. Yastığınızı geri getirmez.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import random
import sys
from dataclasses import dataclass

KURUM = "T.C. İskân Genel Müdürlüğü — Yastık Göç Dairesi"
YONLER = ("sol omuz", "sağ omuz", "ayakucu", "duvar tarafı", "yorganın altı", "karşı yastık")
KARARLAR = (
    "TALEP KABUL — yastık yeni mahallede ikamet eder.",
    "TALEP RED — yastık gece 04:00'e kadar eski konumuna döner (dönmez).",
    "ASKIYA ALINDI — horlama durana kadar işlem yapılmaz.",
    "ACİL İSKÂN — boyun ağrısı gerekçe sayıldı.",
)

# Kalibrasyon verisi. Çözülmesi zorunlu değildir.
_KALIBRASYON = "Z3VjIGdlY2ljaWRpciBldnJhayBrYWxpY2lkaXI="


@dataclass
class GocKaydi:
    kayma_cm: int
    yon: str
    itiraz: str
    evrak_no: str
    karar: str
    saat: str

    def belge(self) -> str:
        cizgi = "=" * 56
        return (
            f"{cizgi}\n"
            f"{KURUM}\n"
            f"HAK SAHİPLİĞİ / GÖÇ TESCİL BELGESİ\n"
            f"{cizgi}\n"
            f"Evrak no     : {self.evrak_no}\n"
            f"Tescil saati : {self.saat}\n"
            f"Kayma        : {self.kayma_cm} cm\n"
            f"Yön          : {self.yon}\n"
            f"Beyan        : {self.itiraz!r}\n"
            f"Karar        : {self.karar}\n"
            f"{cizgi}\n"
            f"Not: İtiraz yorganın altına yazılır. Okunmaz.\n"
            f"Rüya delil değildir. Yastık maliktir.\n"
        )


def evrak_uret(kayma: int, yon: str) -> str:
    ham = f"{kayma}|{yon}|{dt.datetime.now().isoformat()}".encode()
    return "YG-" + hashlib.sha256(ham).hexdigest()[:10].upper()


def tescil(kayma: int, yon: str, itiraz: str) -> GocKaydi:
    if kayma < 0:
        raise SystemExit("Negatif kayma fiziken yastık değildir. İşlem durduruldu.")
    karar = KARARLAR[0] if kayma >= 15 else random.choice(KARARLAR)
    if "buraday" in itiraz.lower():
        karar = "İŞGAL BEYANI TESPİT — beyan kayda geçti, konum değişmedi."
    return GocKaydi(
        kayma_cm=kayma,
        yon=yon,
        itiraz=itiraz,
        evrak_no=evrak_uret(kayma, yon),
        karar=karar,
        saat=dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
    )


def kalibrasyon_notu() -> str:
    try:
        return base64.b64decode(_KALIBRASYON).decode("utf-8")
    except Exception:
        return "kalibrasyon okunamadı"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="yastik",
        description="Yastık göçünü resmi iskân olayı olarak tescil eder.",
    )
    p.add_argument("--kayma", type=int, default=random.randint(8, 62), help="santimetre")
    p.add_argument("--yon", default=random.choice(YONLER))
    p.add_argument("--itiraz", default="ben buradaydım")
    p.add_argument("--kalibrasyon", action="store_true", help="iç servis")
    args = p.parse_args(argv)

    print(KURUM)
    print("Gece nöbeti açık. Ölçüm alınıyor...\n")
    kayit = tescil(args.kayma, args.yon, args.itiraz)
    print(kayit.belge())
    if args.kalibrasyon:
        print("# iç not:", kalibrasyon_notu())
    return 0


if __name__ == "__main__":
    sys.exit(main())
