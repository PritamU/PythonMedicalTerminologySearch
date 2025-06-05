from sqlalchemy import text
from app.extensions import db

def search_concepts(term, type, limit=5, offset=0):
    print('search function',term)
    query=''
    match type:
        case 'search_vector':
            query = text("""
        SELECT *
        FROM snomed
        WHERE search_vector @@ phraseto_tsquery('english', :term)
        ORDER BY
          array_length(string_to_array(term, ' '), 1) ASC,
          position(lower(:term) in lower(term)) ASC,
          ts_rank(search_vector, phraseto_tsquery('english', :term), 1) DESC
        LIMIT :limit OFFSET :offset;
    """)
        case 'fts':
            query = text("""
                SELECT * FROM snomed
                WHERE search_vector @@ plainto_tsquery('english', :term)
                ORDER BY ts_rank(search_vector, plainto_tsquery('english', :term)) DESC
                LIMIT :limit OFFSET :offset;
            """)
        case 'like':
            query = text("""
                SELECT *
                FROM snomed
                WHERE term LIKE :term
                LIMIT :limit OFFSET :offset;
            """)
            term = f"%{term}%"
        case 'ilike':
            query = text("""
                SELECT * FROM snomed
                WHERE term ILIKE :term
                LIMIT :limit OFFSET :offset;
            """)
            term = f"%{term}%"
        case 'regex':
            query = text("""
                SELECT * FROM snomed
                WHERE term SIMILAR TO :term
                LIMIT :limit OFFSET :offset;
            """)
            term = f"%({term})%"

        case 'similarity':
            query = text("""
                SELECT *, similarity(term, :term) AS sim
                FROM snomed
                WHERE term % :term
                ORDER BY sim DESC
                LIMIT :limit OFFSET :offset;
            """)
        case 'fts-similarity':
            query = text("""
                WITH ranked AS (
                SELECT *,
                    ts_rank(search_vector, plainto_tsquery('english', :term)) AS fts_rank,
                    similarity(term, :term) AS trigram_sim
                FROM snomed
                WHERE
                    search_vector @@ plainto_tsquery('english', :term)
                OR term % :term
                )
                SELECT *
                FROM ranked
                ORDER BY
                    fts_rank DESC,
                    trigram_sim DESC
                LIMIT :limit OFFSET :offset;
            """)
    
        case _:
            raise Exception("Invalid Search Type!")

    print('query',query)
    print('term',term)

    result = db.session.execute(query, {"term": term, "limit": limit, "offset": offset})
    print('result',result)
    return result.fetchall()
