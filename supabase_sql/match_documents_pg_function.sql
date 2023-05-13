create or replace function public.match_documents(
  query_embedding vector(1536),
  similarity_threshold float,
  match_count int
)
returns table(
  id bigint,
  content text,
  source text,
  similarity float
)
language sql
as $$
select id, content, source, 1 - (documents.embedding<=>query_embedding) as similarity
from documents
where 1 - (documents.embedding<=>query_embedding)>similarity_threshold
order by documents.embedding<=>query_embedding
limit match_count;
$$;