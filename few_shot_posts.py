import pandas as pd
import json

class PostDataset:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.tags_list = None
        self.load_data(file_path)

    def load_data(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            # categorize length
            self.df['length_category'] = self.df['line_count'].apply(self._categorize_length)
            # collect unique tags
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.tags_list = list(set(all_tags))

    def _categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.tags_list

    # Renamed to match your generator
    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda t: tag in t)) &
            (self.df['language'] == language) &
            (self.df['length_category'] == length)
        ]
        return df_filtered.to_dict(orient='records')


if __name__ == "__main__":
    dataset = PostDataset()
    print(dataset.get_tags())
    sample_posts = dataset.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(sample_posts)
