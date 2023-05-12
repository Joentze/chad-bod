-- ADD THIS TO CREATE VECTOR TABLE ON SUPABASE
create table documents(
  id bigserial primary key,
  content text,
  source text,
  embedding vector (1536)
)