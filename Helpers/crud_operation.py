import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def get_value_float(conn, col, table, addition_join = "", addition_where = "", addition_group_by = ""):
    cur = conn.cursor()
    cur.execute(f'''SELECT {col} FROM {table} {addition_join} {addition_where} {addition_group_by};''')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    return float(rows[0][0])


def update_value(conn, col, table, value, where_clause):
    cur = conn.cursor()
    cur.execute(f'''UPDATE {table} SET {col} = {value} {where_clause};''')
    conn.commit()
    logger.info(f'Value update for {col} in {table} by {value} {where_clause}')
    cur.close()
    
def insert_row(conn, table,cols, values):
    cur = conn.cursor()
    values = [str(i) for i in values]
    cur.execute(f""" INSERT INTO {table}({','.join(cols)}) VALUES({','.join(values)});""")
    conn.commit()
    logger.info(f'Insertion Complete')
    cur.close()

def delete_row(conn, table, where_clause):
    pass
