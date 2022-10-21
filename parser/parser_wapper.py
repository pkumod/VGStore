import time

import rdflib.plugins.sparql.algebra as algebra
import rdflib.term as term

import parser


def process_query(query: str) -> (str, dict):
    start_time = time.time()
    q = query.replace('mm.', parser.MM_INDICATOR)
    query_tree = parser.parseQuery(q)
    if query_tree[1].name != 'SelectQuery':
        raise Exception('Does not support query type:', query_tree[1].name)
    _, extended_proj = process_proj(query_tree[1].projection)
    _, extended_triples, extended_filters = process_where(query_tree[1].where)
    if 'orderby' in query_tree[1]:
        _, extended_orderby = process_orderby(query_tree[1].orderby)
    if 'groupby' in query_tree[1]:
        process_groupby(query_tree[1].groupby)
    query_algebra = algebra.translateQuery(query_tree)
    qs = algebra.translateAlgebra(query_algebra)
    if 'orderby' in query_tree:
        return qs, {"extended_proj": extended_proj, "extended_triples": extended_triples,
                    "extended_filters": extended_filters, "extended_orderby": extended_orderby}
    print('Query translation time:', time.time() - start_time * 1000, 'ms')
    return qs, {"extended_proj": extended_proj, "extended_triples": extended_triples,
                "extended_filters": extended_filters}


def process_groupby(groupby):
    for condition in groupby.condition:
        if isinstance(condition, term.Variable) and condition.startswith(parser.MM_INDICATOR):
            raise Exception('Extended variable found in GROUPBY clause but not support now')


def process_orderby(orderby):
    extended_orderby = []
    for condition in orderby.condition:
        if traverse_expr(condition.expr, lambda x: x.startswith(parser.MM_INDICATOR)):
            extended_orderby.append(condition)
    for condition in extended_orderby:
        orderby.condition.remove(condition)
    return orderby, extended_orderby


def process_where(where):
    extended_triples = []
    extended_filters = []
    for part in where.part:
        if part.name == 'TriplesBlock':
            for triple in part.triples:
                s, p, o = triple
                if (isinstance(s, term.Variable) and s.startswith(parser.MM_INDICATOR)) or \
                        (isinstance(o, term.Variable) and o.startswith(parser.MM_INDICATOR)):
                    raise Exception('Extended variable found in subject or object but not support now')
                if isinstance(p, term.Variable) and p.startswith(parser.MM_INDICATOR):
                    extended_triples.append(triple)
                    continue
                # Find extended predicate.
                if p.name == 'PathAlternative' and 'part' in p and 'part' in p.part[0] \
                        and p.part[0].part[0].part.startswith(parser.MM_INDICATOR):
                    extended_triples.append(triple)
                    continue
            for triple in extended_triples:
                part.triples.remove(triple)
        # Only the Conditional or Expression Filter will be considered.
        if part.name == 'Filter' and part.expr.name == 'ConditionalOrExpression':
            if traverse_expr(part.expr, lambda x: x.startswith(parser.MM_INDICATOR)):
                extended_filters.append(part)
                where.part.remove(part)
        if 'Union' in part.name:
            raise Exception('UNION/NestedQuery clause is not support now')
    return where, extended_triples, extended_filters


def process_proj(projection):
    extended_projs = []
    for proj in projection:
        if 'var' in proj:
            if proj.var.startswith(parser.MM_INDICATOR):
                extended_projs.append(proj)
        if 'expr' in proj:
            if traverse_expr(proj, lambda x: x.startswith(parser.MM_INDICATOR)):
                raise Exception('Extended variable found in composite projection but not support now')
    for proj in extended_projs:
        projection.remove(proj)
    return projection, extended_projs


def traverse_expr(expr, func):
    flag = None
    if 'evar' in expr:
        flag = func(expr['evar'])
    if 'var' in expr:
        flag = func(expr['var'])
    if 'expr' in expr:
        if isinstance(expr['expr'], term.Variable):
            flag = func(expr['expr'])
        else:
            return traverse_expr(expr['expr'], func)
    if flag:
        return flag
    if 'vars' in expr:
        print(expr)
        return traverse_expr(expr['vars'], func)


if __name__ == "__main__":
    q = """select ?x ?y ?mm.sim ?color {
               ?x <hasName> "cat".
               ?y <hasName> "dog".
               ?x <mm.color> ?color.
               ?x ?mm.sim ?y.
               FILTER regex(str(?x), "OB_58") .
               FILTER(?mm.sim > 0.7)
           } GROUP BY ?x ?y
            ORDER BY DESC(?mm.sim) ?x"""
    print(process_query(q))
