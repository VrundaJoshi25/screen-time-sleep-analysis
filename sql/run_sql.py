"""SQL layer (Act 8): load clean data into SQLite and run analysis SQL files.
Usage:
    python sql/run_sql.py                       # demo on NHANES working data
    python sql/run_sql.py <csv> <table> <sqlfile>   # generic
Every analysis question is answered twice: once in pandas, once in SQL.
"""
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "clean", "sleep_project.db")


def load_csv_to_sqlite(csv_path, table, db=DB):
    import pandas as pd
    df = pd.read_csv(csv_path)
    con = sqlite3.connect(db)
    df.to_sql(table, con, if_exists="replace", index=False)
    con.close()
    return len(df)


def run_sql_file(sql_path, db=DB):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    script = open(sql_path, encoding="utf-8").read()
    outputs = []
    for chunk in script.split(";"):
        lines = [l for l in chunk.splitlines() if l.strip()]
        title = ""
        sql_lines = []
        for l in lines:
            if l.strip().startswith("--") and not sql_lines:
                title = l.strip("- ").strip()
            else:
                sql_lines.append(l)
        stmt = "\n".join(sql_lines).strip()
        if not stmt:
            continue
        try:
            cur = con.execute(stmt)
            rows = [dict(r) for r in cur.fetchall()]
            outputs.append((title or stmt.splitlines()[0][:60], rows))
        except Exception as e:
            outputs.append(("FAILED: " + stmt.splitlines()[0][:60], [{"error": str(e)}]))
    con.close()
    return outputs


if __name__ == "__main__":
    if len(sys.argv) == 4:
        n = load_csv_to_sqlite(sys.argv[1], sys.argv[2])
        print("loaded %d rows into table '%s'" % (n, sys.argv[2]))
        sqlf = sys.argv[3]
    else:
        n = load_csv_to_sqlite(os.path.join(ROOT, "data", "clean", "nhanes_work.csv"), "nhanes")
        print("loaded %d rows into table 'nhanes'" % n)
        sqlf = os.path.join(ROOT, "sql", "analysis_nhanes.sql")
    for title, rows in run_sql_file(sqlf):
        print("\n-- %s" % title)
        for r in rows[:15]:
            print("  ", r)
