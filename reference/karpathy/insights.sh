# Capture and structure Karpathy's latest blog post
wind "Karpathy latest blog, focus on insights"
# → Creates karpathy_blog.md with structured insights

# Extract just the insights section
unwind karpathy_blog --extract insights  
# → Creates insights.md, updates karpathy_blog.md

# Generate a new blog post about Wind based on those insights
wind "Wind blog post inspired by Karpathy's insights" | illuminate
# → Captures intent AND immediately renders to blog post