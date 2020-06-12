### Dream Bank Emotion Analysis ###

# Packages
# install.packages("syuzhet")
library(syuzhet)

# Get NRC Emotional Scores
df = read.csv("dreams_umap_df.csv")

# Get number of words per row
df$nb_words = lengths(gregexpr("[[:>:]]",df$content, perl=TRUE))

# Get NRC Sentiment Scores
dreams = df$content
nrc_scores = get_nrc_sentiment(dreams)

# Concat NRC Scores with Dreams DataFrame
df_nrc_scores = cbind(df, nrc_scores)

# Save to CSV File
write.csv(df_nrc_scores, "dreams_syuzhet_df.csv")
