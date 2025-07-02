from supabase import create_client
import os

SUPABASE_URL = os.environ.get("https://vqthalnqpmsfldpovlrp.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxdGhhbG5xcG1zZmxkcG92bHJwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTQ0MjU3OSwiZXhwIjoyMDY3MDE4NTc5fQ.2b0xel2abCcRNsQio4uR6E_5ImeHaYIT56zARaHEmqw")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
