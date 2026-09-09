from __future__ import annotations

MODULE_WEIGHTS = {
    "vibe":1.0,
    "acoustic":0.8,
    "thermal":0.9,
    "power":1.0,
    "circuit":1.0
}

def fuse(results: dict[str, dict]) -> dict:
    valid = []
    for name, result in results.items():
        if isinstance(result, dict) and "health_score" in result:
            w = MODULE_WEIGHTS.get(name,1.0)
            valid.append((float(result["health_score"]),w,name,result))
    if not valid:
        return {
            "module":"X-Repair Core",
            "health_score":0.0,
            "status":"donnees_insuffisantes",
            "priority":"aucune_decision",
            "contributors":[]
        }
    total_w = sum(w for _,w,_,_ in valid)
    weighted = sum(score*w for score,w,_,_ in valid)/total_w
    worst = min(valid, key=lambda x:x[0])
    if weighted >= 85:
        status, priority = "bon", "surveillance_normale"
    elif weighted >= 65:
        status, priority = "surveillance", "controle_planifie"
    elif weighted >= 40:
        status, priority = "degrade", "inspection_prioritaire"
    else:
        status, priority = "critique", "inspection_immediate"
    return {
        "module":"X-Repair Core",
        "health_score":round(weighted,1),
        "status":status,
        "priority":priority,
        "worst_module":worst[2],
        "contributors":[
            {"name":name,"health_score":score,"weight":w}
            for score,w,name,_ in valid
        ]
    }
