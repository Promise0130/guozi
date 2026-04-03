import csv
with open('delivery/guozi_monthly_operation_v1_20260402.csv', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    for row in r:
        c = row.get('confidence','')
        u = row.get('uev_level','')
        rid = row.get('record_id','')
        ed = row.get('extraction_date','')
        if c == '2026-04-02' or u == '0.90':
            print("BAD:", rid, "conf="+c, "uev="+u, "extr_date="+ed)
