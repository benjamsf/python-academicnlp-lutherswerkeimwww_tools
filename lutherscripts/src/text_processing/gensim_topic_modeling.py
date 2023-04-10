import json
import os
import gensim
from gensim import corpora
from tqdm import tqdm

__author__ = "benjamsf"
__license__ = "MIT"

def main(source_path, dictionary_path, num_topics, num_passes, destination_path):
    # Load the corpus from the file
    corpus = gensim.corpora.MmCorpus(source_path)

    # Load the dictionary from the file
    dictionary = corpora.Dictionary.load(dictionary_path)

   # Train the LDA model on the corpus
    with tqdm(desc="Step 1 - Training LDA model:", total=num_passes) as pbar:
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=num_topics,
                                               passes=num_passes,
                                               callbacks=[pbar.update])

    # Extract the topics and their associated words
    topics = []
    for topic_num, topic_words in tqdm(lda_model.show_topics(num_topics=num_topics, formatted=False),
                                        desc='Step 2 - Extracting topics:'):
        words = [word for word, _ in topic_words]
        topics.append({'topic_num': topic_num, 'words': words})

    # Save the topics as a JSON file
    with open(destination_path, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    # Print a message to confirm that the file has been saved
    print(f'The topic modeling results have been saved as {destination_path}')

