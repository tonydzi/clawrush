"""bench.py — пилот «вторая память на другом движке».

Вход: замороженный срез нашего живого индекса (_brain_e5.npy + _brain_e5_meta.pkl, N чанков,
768-d), один и тот же для всех движков. Запросы = held-out векторы чанков (leave-one-out),
gold = точный brute-force top-K по косинусу на numpy. Так сравниваются ДВИЖКИ при одном и
том же retrieval (поправка Codex 2016481), а не эмбеддеры.

Для каждого движка: ingest_s · index_s · q_p50_ms · q_p95_ms · recall@10 vs exact ·
disk_mb · filtered-запрос (source_type) работает? · update/delete работает? · restart:
переоткрыл файл и получил тот же ответ?

Движки (все embedded, без сервера, потому что docker-демон на хабе не поднят 05.11):
  sqlite_numpy  наша текущая схема (SQLite метаданные + numpy brute force) = baseline
  sqlite_vec    sqlite-vec (vec0 virtual table, brute force внутри SQLite)
  duckdb        DuckDB + VSS (HNSW)
  chdb          chDB = embedded ClickHouse (cosineDistance brute force; то, на чём auxten/clickmem)
  lancedb       LanceDB (IVF_PQ индекс при N>=5000, иначе flat)
  qdrant        qdrant-client local mode (HNSW на диске, без сервера)

Запуск: .venv/Scripts/python bench.py --n 20000 --queries 200 [--engines a,b]
Выход: results.json + results.md рядом. Паспорт: вход numpy+pkl из E:\\Obsidian\\_imports,
зовёт человек/сессия, ломается при смене формата meta (dict с 'path','source_type','date').
рельса: нет (чистый код, 0 LLM).
Machine: hub · Agent: Claude · Operator: Anton · 2026-11-05
"""
import argparse, json, os, pickle, shutil, sys, time, traceback
from pathlib import Path
import numpy as np

IMP = Path(os.environ.get('BRAIN_IMPORTS', r'<vault-imports>'))
HERE = Path(__file__).resolve().parent
WORK = Path(os.environ.get('PILOT_WORK', str(HERE / 'work')))
K = 10


def load_corpus(n, seed=7):
    emb = np.load(IMP / '_brain_e5.npy', mmap_mode='r')
    meta = pickle.load(open(IMP / '_brain_e5_meta.pkl', 'rb'))
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(emb.shape[0], size=min(n, emb.shape[0]), replace=False))
    X = np.ascontiguousarray(emb[idx], dtype=np.float32)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    rows = []
    for i, j in enumerate(idx):
        m = meta[int(j)]
        rows.append({'id': i, 'path': str(m.get('path', ''))[-200:], 'title': str(m.get('title', ''))[:200],
                     'source_type': str(m.get('source_type', '') or 'note'), 'date': str(m.get('date', '') or ''),
                     'snippet': str(m.get('snippet', ''))[:300]})
    return X, rows


def gold(X, qids, filt=None):
    """exact top-K по косинусу (X нормирован). filt: bool mask допустимых строк."""
    out = {}
    for q in qids:
        s = X @ X[q]          # сам запрос входит в gold: движки его тоже возвращают (top-1, расстояние 0)
        if filt is not None:
            s = np.where(filt, s, -2.0)
        out[q] = set(np.argpartition(-s, K)[:K].tolist())
    return out


def recall(res, gd):
    return float(np.mean([len(set(res[q]) & gd[q]) / K for q in gd]))


def pct(xs, p):
    return float(np.percentile(np.array(xs) * 1000.0, p))


def dir_size_mb(p):
    p = Path(p)
    if p.is_file():
        return round(p.stat().st_size / 1e6, 1)
    return round(sum(f.stat().st_size for f in p.rglob('*') if f.is_file()) / 1e6, 1)


# ---------------------------------------------------------------- engines
class Engine:
    name = 'base'
    def __init__(self, dim): self.dim = dim; self.path = WORK / self.name
    def reset(self):
        if self.path.exists():
            shutil.rmtree(self.path, ignore_errors=True) if self.path.is_dir() else self.path.unlink()
    def ingest(self, X, rows): ...
    def index(self): pass
    def query(self, v, k=K, source_type=None): ...
    def update(self, i, v): raise NotImplementedError
    def delete(self, i): raise NotImplementedError
    def reopen(self): pass
    def close(self): pass
    def size_mb(self): return dir_size_mb(self.path)


class SqliteNumpy(Engine):
    name = 'sqlite_numpy'
    def __init__(self, dim):
        super().__init__(dim); self.path = WORK / 'sqlite_numpy'; self.path.mkdir(parents=True, exist_ok=True)
    def reset(self):
        shutil.rmtree(self.path, ignore_errors=True); self.path.mkdir(parents=True, exist_ok=True)
    def ingest(self, X, rows):
        import sqlite3
        self.X = X.copy(); np.save(self.path / 'emb.npy', self.X)
        self.con = sqlite3.connect(self.path / 'meta.db')
        self.con.execute('create table m(id integer primary key, path, title, source_type, date)')
        self.con.executemany('insert into m values(?,?,?,?,?)', [(r['id'], r['path'], r['title'], r['source_type'], r['date']) for r in rows])
        self.con.commit()
        self.st = np.array([r['source_type'] for r in rows])
    def query(self, v, k=K, source_type=None):
        s = self.X @ v
        if source_type: s = np.where(self.st == source_type, s, -2.0)
        return np.argpartition(-s, k)[:k].tolist()
    def update(self, i, v): self.X[i] = v
    def delete(self, i): self.X[i] = 0; self.con.execute('delete from m where id=?', (i,)); self.con.commit()
    def reopen(self):
        self.con.close(); self.X = np.load(self.path / 'emb.npy')
        import sqlite3; self.con = sqlite3.connect(self.path / 'meta.db')
        self.st = np.array([r[0] for r in self.con.execute('select source_type from m order by id')] + [''] * (len(self.X) - self.con.execute('select count(*) from m').fetchone()[0]))
    def close(self): self.con.close()


class SqliteVec(Engine):
    name = 'sqlite_vec'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'sqlite_vec.db'
    def _open(self):
        import sqlite3, sqlite_vec
        self.con = sqlite3.connect(self.path); self.con.enable_load_extension(True); sqlite_vec.load(self.con); self.con.enable_load_extension(False)
    def ingest(self, X, rows):
        import sqlite_vec
        self._open()
        self.con.execute(f'create virtual table v using vec0(id integer primary key, emb float[{self.dim}], source_type text)')
        self.con.execute('create table m(id integer primary key, path, title, date)')
        with self.con:
            self.con.executemany('insert into v(id, emb, source_type) values(?,?,?)', [(r['id'], sqlite_vec.serialize_float32(X[r['id']].tolist()), r['source_type']) for r in rows])
            self.con.executemany('insert into m values(?,?,?,?)', [(r['id'], r['path'], r['title'], r['date']) for r in rows])
    def query(self, v, k=K, source_type=None):
        import sqlite_vec
        q = sqlite_vec.serialize_float32(v.tolist())
        if source_type:
            sql = 'select id from v where emb match ? and k=? and source_type=? order by distance'
            return [r[0] for r in self.con.execute(sql, (q, k, source_type))]
        return [r[0] for r in self.con.execute('select id from v where emb match ? and k=? order by distance', (q, k))]
    def update(self, i, v):
        import sqlite_vec
        with self.con: self.con.execute('update v set emb=? where id=?', (sqlite_vec.serialize_float32(v.tolist()), i))
    def delete(self, i):
        with self.con: self.con.execute('delete from v where id=?', (i,)); self.con.execute('delete from m where id=?', (i,))
    def reopen(self): self.con.close(); self._open()
    def close(self): self.con.close()


class DuckDB(Engine):
    name = 'duckdb'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'duck.db'
    def _open(self):
        import duckdb
        self.con = duckdb.connect(str(self.path)); self.con.execute('install vss; load vss;')
        self.con.execute("set hnsw_enable_experimental_persistence = true")
    def ingest(self, X, rows):
        self._open()
        self.con.execute(f'create table m(id integer primary key, path varchar, title varchar, source_type varchar, date varchar, emb float[{self.dim}])')
        self.con.executemany('insert into m values(?,?,?,?,?,?)', [(r['id'], r['path'], r['title'], r['source_type'], r['date'], X[r['id']].tolist()) for r in rows])
    def index(self):
        self.con.execute("create index hnsw_idx on m using hnsw(emb) with (metric='cosine')")
    def query(self, v, k=K, source_type=None):
        if source_type:
            sql = f"select id from m where source_type=? order by array_cosine_distance(emb, ?::float[{self.dim}]) limit {k}"
            return [r[0] for r in self.con.execute(sql, [source_type, v.tolist()]).fetchall()]
        sql = f"select id from m order by array_cosine_distance(emb, ?::float[{self.dim}]) limit {k}"
        return [r[0] for r in self.con.execute(sql, [v.tolist()]).fetchall()]
    def update(self, i, v): self.con.execute('update m set emb=? where id=?', [v.tolist(), i])
    def delete(self, i): self.con.execute('delete from m where id=?', [i])
    def reopen(self): self.con.close(); self._open()
    def close(self): self.con.close()


class ChDB(Engine):
    name = 'chdb'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'chdb'
    def _open(self):
        import chdb
        self.path.mkdir(parents=True, exist_ok=True)
        self.s = chdb.session.Session(str(self.path))
        self.s.query('create database if not exists mem')
    def ingest(self, X, rows):
        self._open()
        self.s.query(f'create table if not exists mem.m (id UInt32, path String, title String, source_type LowCardinality(String), date String, emb Array(Float32)) engine=MergeTree order by id')
        import csv, io
        # вставка батчами через VALUES (chdb принимает большие тексты)
        B = 2000
        for a in range(0, len(rows), B):
            vals = []
            for r in rows[a:a + B]:
                e = ','.join(f'{x:.6f}' for x in X[r['id']].tolist())
                vals.append("(%d,%s,%s,%s,%s,[%s])" % (r['id'], _q(r['path']), _q(r['title']), _q(r['source_type']), _q(r['date']), e))
            self.s.query('insert into mem.m values ' + ','.join(vals))
    def query(self, v, k=K, source_type=None):
        e = '[' + ','.join(f'{x:.6f}' for x in v.tolist()) + ']'
        w = f"where source_type={_q(source_type)}" if source_type else ''
        res = self.s.query(f'select id from mem.m {w} order by cosineDistance(emb, {e}) limit {k}', 'CSV')
        return [int(x) for x in str(res).split() if x.strip()]
    def update(self, i, v):
        e = '[' + ','.join(f'{x:.6f}' for x in v.tolist()) + ']'
        self.s.query(f'alter table mem.m update emb={e} where id={i} settings mutations_sync=2')
    def delete(self, i): self.s.query(f'alter table mem.m delete where id={i} settings mutations_sync=2')
    def reopen(self):
        self.s.close(); self._open()
    def close(self): self.s.close()


def _q(s):
    return "'" + str(s).replace('\\', '\\\\').replace("'", "\\'") + "'"


class Lance(Engine):
    name = 'lancedb'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'lance'
    def _open(self):
        import lancedb
        self.db = lancedb.connect(str(self.path)); self.t = self.db.open_table('m') if 'm' in self.db.table_names() else None
    def ingest(self, X, rows):
        import lancedb
        self.db = lancedb.connect(str(self.path))
        data = [{'id': r['id'], 'path': r['path'], 'title': r['title'], 'source_type': r['source_type'], 'date': r['date'], 'vector': X[r['id']].tolist()} for r in rows]
        self.t = self.db.create_table('m', data=data, mode='overwrite')
    def index(self):
        # LANCE_INDEX=flat -> без индекса (точный скан); иначе IVF_PQ (первый прогон 05.11: recall 0.63, PQ 48 на 768-d = сильные потери)
        if os.environ.get('LANCE_INDEX', 'ivfpq') == 'flat':
            return
        if self.t.count_rows() >= 5000:
            self.t.create_index(metric='cosine', num_partitions=64, num_sub_vectors=48)
    def query(self, v, k=K, source_type=None):
        q = self.t.search(v.tolist()).metric('cosine').limit(k)
        if source_type: q = q.where(f"source_type = '{source_type}'", prefilter=True)
        return [int(r['id']) for r in q.to_list()]
    def update(self, i, v): self.t.update(where=f'id = {i}', values={'vector': v.tolist()})
    def delete(self, i): self.t.delete(f'id = {i}')
    def reopen(self): self._open()


class Qdrant(Engine):
    name = 'qdrant'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'qdrant'
    def _open(self):
        from qdrant_client import QdrantClient
        self.c = QdrantClient(path=str(self.path))
    def ingest(self, X, rows):
        from qdrant_client import models
        self._open()
        self.c.recreate_collection('m', vectors_config=models.VectorParams(size=self.dim, distance=models.Distance.COSINE))
        B = 1000
        for a in range(0, len(rows), B):
            pts = [models.PointStruct(id=r['id'], vector=X[r['id']].tolist(), payload={'path': r['path'], 'title': r['title'], 'source_type': r['source_type'], 'date': r['date']}) for r in rows[a:a + B]]
            self.c.upsert('m', pts)
    def query(self, v, k=K, source_type=None):
        from qdrant_client import models
        f = models.Filter(must=[models.FieldCondition(key='source_type', match=models.MatchValue(value=source_type))]) if source_type else None
        res = self.c.query_points('m', query=v.tolist(), limit=k, query_filter=f).points
        return [int(p.id) for p in res]
    def update(self, i, v):
        from qdrant_client import models
        self.c.update_vectors('m', [models.PointVectors(id=i, vector=v.tolist())])
    def delete(self, i):
        from qdrant_client import models
        self.c.delete('m', points_selector=models.PointIdsList(points=[i]))
    def reopen(self): self.c.close(); self._open()
    def close(self): self.c.close()


class Pgvector(Engine):
    """Postgres + pgvector через embedded-postgres (pip, без Docker): HNSW cosine, фильтр в WHERE,
    hnsw.iterative_scan=relaxed_order чтобы фильтр не возвращал <k (pgvector >= 0.8).
    Добавлено сессией f9a9c736 05.11 (Machine: hub)."""
    name = 'pgvector'
    def __init__(self, dim): super().__init__(dim); self.path = WORK / 'pgvector'; self.pg = None; self.conn = None
    def _open(self):
        import psycopg
        from embedded_postgres import get_server
        from pgvector.psycopg import register_vector
        if self.pg is None:
            self.path.mkdir(parents=True, exist_ok=True)
            self.pg = get_server(self.path)
            self.dsn = self.pg.get_uri()
        self.conn = psycopg.connect(self.dsn, autocommit=True)
        self.conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(self.conn)
    def ingest(self, X, rows):
        self._open()
        self.conn.execute('DROP TABLE IF EXISTS m')
        self.conn.execute(f'CREATE TABLE m (id int PRIMARY KEY, source_type text, v vector({self.dim}))')
        with self.conn.cursor() as cur:
            with cur.copy('COPY m (id, source_type, v) FROM STDIN WITH (FORMAT BINARY)') as cp:
                cp.set_types(['int4', 'text', 'vector'])
                for r in rows:
                    cp.write_row((r['id'], r['source_type'], X[r['id']]))
    def index(self):
        self.conn.execute('CREATE INDEX m_hnsw ON m USING hnsw (v vector_cosine_ops)')
    def query(self, v, k=K, source_type=None):
        with self.conn.cursor() as cur:
            cur.execute('SET hnsw.iterative_scan = relaxed_order')
            if source_type:
                cur.execute('SELECT id FROM m WHERE source_type = %s ORDER BY v <=> %s LIMIT %s', (source_type, v, k))
            else:
                cur.execute('SELECT id FROM m ORDER BY v <=> %s LIMIT %s', (v, k))
            return [int(r[0]) for r in cur.fetchall()]
    def update(self, i, v): self.conn.execute('UPDATE m SET v = %s WHERE id = %s', (v, i))
    def delete(self, i): self.conn.execute('DELETE FROM m WHERE id = %s', (i,))
    def reopen(self):
        self.conn.close(); self.pg.cleanup(); self.pg = None; self._open()
    def close(self):
        try:
            self.conn.close()
        finally:
            if self.pg is not None: self.pg.cleanup(); self.pg = None


ENGINES = {e.name: e for e in [SqliteNumpy, SqliteVec, DuckDB, ChDB, Lance, Qdrant, Pgvector]}


# ---------------------------------------------------------------- run
def run_engine(cls, X, rows, qids, gd, gd_f, ftype):
    r = {'engine': cls.name, 'ok': False}
    eng = cls(X.shape[1])
    try:
        eng.reset()
        t = time.perf_counter(); eng.ingest(X, rows); r['ingest_s'] = round(time.perf_counter() - t, 2)
        t = time.perf_counter(); eng.index(); r['index_s'] = round(time.perf_counter() - t, 2)
        eng.query(X[qids[0]])  # warm
        res, lat = {}, []
        for q in qids:
            t = time.perf_counter(); res[q] = eng.query(X[q]); lat.append(time.perf_counter() - t)
        r['q_p50_ms'] = round(pct(lat, 50), 2); r['q_p95_ms'] = round(pct(lat, 95), 2)
        r['recall@10'] = round(recall(res, gd), 3)
        # filtered
        try:
            resf = {q: eng.query(X[q], source_type=ftype) for q in qids[:50]}
            r['filtered_recall@10'] = round(recall(resf, {q: gd_f[q] for q in qids[:50]}), 3)
        except Exception as e:
            r['filtered_recall@10'] = f'ERR {type(e).__name__}: {str(e)[:80]}'
        # update: подменить вектор строки на вектор запроса -> она обязана стать top-1
        try:
            q = qids[1]; victim = int([i for i in range(len(rows)) if i not in gd[q] and i != q][0])
            eng.update(victim, X[q]); r['update_ok'] = victim in eng.query(X[q], k=2)
        except Exception as e:
            r['update_ok'] = f'ERR {type(e).__name__}: {str(e)[:80]}'
        # delete: убрать top-1 gold и убедиться, что он исчез
        try:
            q = qids[2]; top = eng.query(X[q], k=1)[0]
            eng.delete(top); r['delete_ok'] = top not in eng.query(X[q], k=K)
        except Exception as e:
            r['delete_ok'] = f'ERR {type(e).__name__}: {str(e)[:80]}'
        # restart
        try:
            before = eng.query(X[qids[3]]); eng.reopen(); after = eng.query(X[qids[3]])
            r['restart_same'] = before == after
        except Exception as e:
            r['restart_same'] = f'ERR {type(e).__name__}: {str(e)[:80]}'
        try: eng.close()
        except Exception: pass
        r['disk_mb'] = eng.size_mb()
        r['ok'] = True
    except Exception as e:
        r['error'] = f'{type(e).__name__}: {str(e)[:300]}'; r['trace'] = traceback.format_exc()[-800:]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=20000); ap.add_argument('--queries', type=int, default=200)
    ap.add_argument('--engines', default=','.join(ENGINES)); ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--tag', default='run')
    a = ap.parse_args()
    WORK.mkdir(exist_ok=True)
    X, rows = load_corpus(a.n, a.seed)
    rng = np.random.default_rng(a.seed + 1)
    qids = [int(i) for i in rng.choice(len(rows), size=a.queries, replace=False)]
    st = np.array([r['source_type'] for r in rows])
    ftype = max(set(st.tolist()), key=st.tolist().count)
    gd = gold(X, qids); gd_f = gold(X, qids[:50], filt=(st == ftype))
    out = {'corpus': {'n': len(rows), 'dim': int(X.shape[1]), 'source': str(IMP / '_brain_e5.npy'), 'queries': a.queries, 'filter_type': ftype,
                      'seed': a.seed, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'host': os.environ.get('PILOT_HOST', 'win'), 'tag': a.tag}, 'results': []}
    for name in a.engines.split(','):
        print(f'== {name}', flush=True)
        r = run_engine(ENGINES[name], X, rows, qids, gd, gd_f, ftype)
        print(json.dumps({k: v for k, v in r.items() if k != 'trace'}, ensure_ascii=False), flush=True)
        out['results'].append(r)
        json.dump(out, open(HERE / f'results-{a.tag}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cols = ['engine', 'ok', 'ingest_s', 'index_s', 'q_p50_ms', 'q_p95_ms', 'recall@10', 'filtered_recall@10', 'update_ok', 'delete_ok', 'restart_same', 'disk_mb', 'error']
    md = [f"# memory-db pilots · N={len(rows)} · dim={X.shape[1]} · queries={a.queries} · {out['corpus']['ts']}", '',
          '| ' + ' | '.join(cols) + ' |', '|' + '---|' * len(cols)]
    for r in out['results']:
        md.append('| ' + ' | '.join(str(r.get(c, '')) for c in cols) + ' |')
    (HERE / f'results-{a.tag}.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
