# 06_EDA.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# terminal command to run script:
# python scripts/06_EDA.py \
#     --train_data_path=data/processed/train_data.csv

def load_data(path):
    return pd.read_csv(path)

@click.command()
@click.option('--train_data_path', type=str, required=True, help="Path to training data CSV")
def main(train_data_path):
    try:
        # Load train dataset
        train_df = load_data(train_data_path)

        # train_df.info() as text file
        buffer = StringIO()
        train_df.info(buf=buffer)
        os.makedirs("data/text", exist_ok=True)
        with open("data/text/train_df_info.txt", "w") as f:
            f.write(buffer.getvalue())
        print("Successfully saved train_df info to data/text as a text file")

        # plot: Count of Fake vs. Real News Articles
        counts = train_df['target'].value_counts().sort_index()
        plt.figure(figsize=(6, 1.5)) 
        plt.barh(counts.index, counts.values)
        plt.xlabel('Count')
        plt.ylabel('Label')
        plt.title('Count of true and fake news articles in training data')
        fig_path_1 = "img/fake_real_count.png"
        plt.tight_layout()
        plt.savefig(fig_path_1, dpi=300, bbox_inches="tight")
        print("Successfully saved fake_real_count.png to the img/ folder")

        # processing in preparation for word clouds
        fake_text = train_df[train_df['target'] == 'Fake']['text']
        true_text = train_df[train_df['target'] == 'True']['text']
        # Remove "'s" instances (possessives/contractions)
        fake_text = fake_text.str.replace(r"\bs\b", "", regex=True)
        true_text = true_text.str.replace(r"\bs\b", "", regex=True)
        # remove punctuation
        fake_text = fake_text.str.replace(r'[^\w\s]', '', regex=True)
        true_text = true_text.str.replace(r'[^\w\s]', '', regex=True)
        fake_words = fake_text.str.cat(sep=" ")
        true_words = true_text.str.cat(sep=" ")
        fake_titles = train_df[train_df['target'] == 'Fake']['title']
        true_titles = train_df[train_df['target'] == 'True']['title']
        # remove punctuation
        fake_titles = fake_titles.str.replace(r'[^\w\s]', '', regex=True)
        true_ttitles = true_titles.str.replace(r'[^\w\s]', '', regex=True)
        # Remove "'s" instances (possessives/contractions)
        fake_titles = fake_titles.str.replace(r"\bs\b", "", regex=True)
        true_titles = true_titles.str.replace(r"\bs\b", "", regex=True)
        fake_title_words = fake_titles.str.cat(sep=" ")
        true_title_words = true_titles.str.cat(sep=" ") 

        # plot: news title word cloud for fake news
        wordcloud_title_fake = WordCloud().generate(fake_title_words)
        plt.figure()
        plt.imshow(wordcloud_title_fake, interpolation="bilinear")
        plt.title("Fake articles title words")
        plt.axis("off")
        fig_path_2 = "img/fake_title_word_cloud.png"
        plt.tight_layout()
        plt.savefig(fig_path_2, dpi=300, bbox_inches="tight")
        print("Successfully saved fake_title_word_cloud.png to the img/ folder")

        # plot: news title word cloud for true news
        wordcloud_title_true = WordCloud().generate(true_title_words)
        plt.figure()
        plt.imshow(wordcloud_title_true, interpolation="bilinear")
        plt.title("True articles title words")
        plt.axis("off")
        fig_path_3 = "img/true_title_word_cloud.png"
        plt.tight_layout()
        plt.savefig(fig_path_3, dpi=300, bbox_inches="tight")
        print("Successfully saved true_title_word_cloud.png to the img/ folder")

        # plot: news text word cloud for fake news
        wordcloud_fake = WordCloud(
            background_color='black'
        ).generate(fake_words)
        plt.figure()
        plt.imshow(wordcloud_fake, interpolation="bilinear")
        plt.title("Fake articles text words")
        plt.axis("off")
        fig_path_4 = "img/fake_text_word_cloud.png"
        plt.tight_layout()
        plt.savefig(fig_path_4, dpi=300, bbox_inches="tight",
                    facecolor = 'black')
        print("Successfully saved fake_text_word_cloud.png to the img/ folder")

        # plot: news text word cloud for true news
        wordcloud_true = WordCloud(
            background_color='black'
        ).generate(true_words)
        plt.figure(facecolor='black')
        plt.imshow(wordcloud_true, interpolation="bilinear")
        plt.title("True articles text words")
        plt.axis("off")
        fig_path_5 = "img/true_text_word_cloud.png"
        plt.tight_layout()
        plt.savefig(fig_path_5, dpi=300, bbox_inches="tight",
                    facecolor = 'black')
        print("Successfully saved true_text_word_cloud.png to the img/ folder")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()