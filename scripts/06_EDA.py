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

        # processing in preparation for string length plots
        train_df["title_length"] = train_df["title"].str.len()
        train_df["text_length"] = train_df["text"].str.len()

        # plot: title length distribution for fake and true news
        bins = 30
        plt.figure(figsize=(8, 5))
        for label in train_df['target'].unique():
            subset = train_df[train_df['target'] == label]
            plt.hist(subset['title_length'],
                     bins=bins,
                     alpha=0.6,
                     label=str(label))
        plt.xlabel('Title Length (Number of Words)')
        plt.ylabel('Number of Articles')
        plt.title('Distribution of article title lengths by news type')
        plt.legend(title='News Type')
        fig_path_6 = "img/title_length_dist.png"
        plt.tight_layout()
        plt.savefig(fig_path_6, dpi=300, bbox_inches="tight")
        print("Successfully saved title_length_dist.png to the img/ folder")

        # plot: text length distribution for fake and true news
        filtered_df = train_df[train_df['text_length'] < 12000]
        bins = 30
        plt.figure(figsize=(8, 5))
        for label in filtered_df['target'].unique():
            subset = filtered_df[filtered_df['target'] == label]
            plt.hist(
                subset['text_length'],
                bins=bins,
                alpha=0.6,
                label=str(label)
            )
        plt.xlabel('Text Length (Number of Words)')
        plt.ylabel('Number of Articles')
        plt.title('Distribution of article text lengths by news type')
        plt.legend(title='News Type')
        fig_path_7 = "img/text_length_dist.png"
        plt.tight_layout()
        plt.savefig(fig_path_7, dpi=300, bbox_inches="tight")
        print("Successfully saved text_length_dist.png to the img/ folder")

        # plot: percentage of counts of subject between fake and true news
        number_of_fake = train_df[train_df['target'] == 'Fake'].shape[0]
        number_of_true = train_df[train_df['target'] == 'True'].shape[0]
        plot_df = train_df.groupby(['target', 'subject']).size().reset_index()
        plot_df.columns = ['target', 'subject', 'count']
        plot_df.loc[plot_df['target'] == 'Fake', 'total'] = number_of_fake
        plot_df.loc[plot_df['target'] == 'True', 'total'] = number_of_true
        plot_df['percentage'] = plot_df['count'] / plot_df['total']
        targets = plot_df['target'].unique()
        num_targets = len(targets)
        fig, axes = plt.subplots(
            nrows=num_targets,
            ncols=1,
            figsize=(6, 3.5))
        if num_targets == 1:
            axes = [axes]
        for ax, tgt in zip(axes, targets):
            subset = plot_df[plot_df['target'] == tgt]
            ax.barh(
                subset['subject'],
                subset['percentage'],
                color=None
            )
            ax.set_title(f"Target = {tgt}", fontsize=10) 
            ax.set_ylabel("Subject type", fontsize=10)
            ax.set_xlabel("Percentage of count", fontsize=10)
        plt.suptitle(
            "Percentage of counts of (non-)political news in fake and true news",
            fontsize=12
        )
        fig_path_8 = "img/subject_percentage_count.png"
        plt.tight_layout()
        plt.savefig(fig_path_8, dpi=300, bbox_inches="tight")
        print("Successfully saved subject_percentage_count.png to the img/ folder")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()