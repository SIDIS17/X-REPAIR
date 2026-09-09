from __future__ import annotations
import os, re, shutil, subprocess, tempfile
from dataclasses import dataclass

@dataclass
class NetlistInfo:
    components: int
    resistors: int
    capacitors: int
    inductors: int
    diodes: int
    transistors: int
    sources: int

def parse_netlist(netlist: str) -> NetlistInfo:
    counts = dict(R=0,C=0,L=0,D=0,Q=0,V=0,I=0)
    total = 0
    for raw in netlist.splitlines():
        line = raw.strip()
        if not line or line.startswith(("*",".",";")):
            continue
        first = line[0].upper()
        if first in counts:
            counts[first] += 1
            total += 1
    return NetlistInfo(
        components=total,
        resistors=counts["R"], capacitors=counts["C"], inductors=counts["L"],
        diodes=counts["D"], transistors=counts["Q"],
        sources=counts["V"]+counts["I"]
    )

def static_checks(netlist: str) -> list[dict]:
    issues = []
    if ".end" not in netlist.lower():
        issues.append({"severity":"warning","code":"MISSING_END","message":"Directive .end absente."})
    if not re.search(r"(?mi)^\s*[vi]\w+\s+", netlist):
        issues.append({"severity":"warning","code":"NO_SOURCE","message":"Aucune source V/I détectée."})
    if " 0 " not in (" "+netlist.replace("\n"," ")+" "):
        issues.append({"severity":"warning","code":"GROUND_CHECK","message":"Le nœud de référence 0 n'est pas clairement détecté."})
    if re.search(r"(?mi)^\s*r\w+\s+\S+\s+\S+\s+0(?:\s|$)", netlist):
        issues.append({"severity":"error","code":"ZERO_RESISTOR","message":"Une résistance de 0 Ω est présente; vérifier si c'est intentionnel."})
    return issues

def simulate_ngspice(netlist: str) -> dict:
    exe = shutil.which("ngspice")
    if not exe:
        return {"available":False,"ran":False,"stdout":"","stderr":"ngspice non installé."}
    with tempfile.TemporaryDirectory() as td:
        cir = os.path.join(td,"xrepair.cir")
        log = os.path.join(td,"xrepair.log")
        with open(cir,"w",encoding="utf-8") as f:
            f.write(netlist)
        p = subprocess.run([exe,"-b","-o",log,cir],capture_output=True,text=True,timeout=20)
        content = ""
        if os.path.exists(log):
            with open(log,"r",encoding="utf-8",errors="ignore") as f:
                content = f.read()
        return {
            "available":True,"ran":True,"returncode":p.returncode,
            "stdout":content[-12000:],"stderr":p.stderr[-4000:]
        }

def analyze(netlist: str, run_spice: bool = False) -> dict:
    info = parse_netlist(netlist)
    issues = static_checks(netlist)
    sim = simulate_ngspice(netlist) if run_spice else {"available":bool(shutil.which("ngspice")),"ran":False}
    error_count = sum(1 for x in issues if x["severity"]=="error")
    warning_count = sum(1 for x in issues if x["severity"]=="warning")
    health = max(0.0, 100.0 - 30*error_count - 10*warning_count)
    return {
        "module":"X-Repair Circuit",
        "diagnostic":"netlist_a_verifier" if issues else "structure_netlist_coherente",
        "health_score":health,
        "components":info.__dict__,
        "issues":issues,
        "spice":sim,
        "recommendation":"Corriger les erreurs statiques puis relancer SPICE. Pour un appareil réel, comparer les nœuds mesurés aux valeurs simulées."
    }
